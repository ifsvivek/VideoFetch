import base64
import functools
import re

from .common import InfoExtractor
from ..utils import (
    clean_html,
    determine_ext,
    float_or_none,
    int_or_none,
    make_archive_id,
    mimetype2ext,
    orderedSet,
    parse_age_limit,
    remove_end,
    strip_jsonp,
    try_call,
    unified_strdate,
    url_or_none,
)
from ..utils.traversal import traverse_obj


class ORFRadioIE(InfoExtractor):
    IE_NAME = 'orf:radio'

    STATION_INFO = {
        'fm4': ('fm4', 'fm4', 'orffm4'),
        'noe': ('noe', 'oe2n', 'orfnoe'),
        'wien': ('wie', 'oe2w', 'orfwie'),
        'burgenland': ('bgl', 'oe2b', 'orfbgl'),
        'ooe': ('ooe', 'oe2o', 'orfooe'),
        'steiermark': ('stm', 'oe2st', 'orfstm'),
        'kaernten': ('ktn', 'oe2k', 'orfktn'),
        'salzburg': ('sbg', 'oe2s', 'orfsbg'),
        'tirol': ('tir', 'oe2t', 'orftir'),
        'vorarlberg': ('vbg', 'oe2v', 'orfvbg'),
        'oe3': ('oe3', 'oe3', 'orfoe3'),
        'oe1': ('oe1', 'oe1', 'orfoe1'),
    }
    _STATION_RE = '|'.join(map(re.escape, STATION_INFO.keys()))

    _VALID_URL = rf'''(?x)
        https?://(?:
            (?P<station>{_STATION_RE})\.orf\.at/player|
            radiothek\.orf\.at/(?P<station2>{_STATION_RE})
        )/(?P<date>[0-9]+)/(?P<show>\w+)'''

    _TESTS = [{
        'url': 'https://radiothek.orf.at/ooe/20220801/OGMO',
        'info_dict': {
            'id': 'OGMO',
            'title': 'Guten Morgen OÖ',
            'description': 'md5:a3f6083399ef92b8cbe2d421b180835a',
        },
        'playlist': [{
            'md5': 'f33147d954a326e338ea52572c2810e8',
            'info_dict': {
                'id': '2022-08-01_0459_tl_66_7DaysMon1_319062',
                'ext': 'mp3',
                'title': 'Guten Morgen OÖ',
                'upload_date': '20220801',
                'duration': 18000,
                'timestamp': 1659322789,
                'description': 'md5:a3f6083399ef92b8cbe2d421b180835a',
            }
        }]
    }, {
        'url': 'https://ooe.orf.at/player/20220801/OGMO',
        'info_dict': {
            'id': 'OGMO',
            'title': 'Guten Morgen OÖ',
            'description': 'md5:a3f6083399ef92b8cbe2d421b180835a',
        },
        'playlist': [{
            'md5': 'f33147d954a326e338ea52572c2810e8',
            'info_dict': {
                'id': '2022-08-01_0459_tl_66_7DaysMon1_319062',
                'ext': 'mp3',
                'title': 'Guten Morgen OÖ',
                'upload_date': '20220801',
                'duration': 18000,
                'timestamp': 1659322789,
                'description': 'md5:a3f6083399ef92b8cbe2d421b180835a',
            }
        }]
    }, {
        'url': 'http://fm4.orf.at/player/20170107/4CC',
        'only_matching': True,
    }, {
        'url': 'https://noe.orf.at/player/20200423/NGM',
        'only_matching': True,
    }, {
        'url': 'https://wien.orf.at/player/20200423/WGUM',
        'only_matching': True,
    }, {
        'url': 'https://burgenland.orf.at/player/20200423/BGM',
        'only_matching': True,
    }, {
        'url': 'https://steiermark.orf.at/player/20200423/STGMS',
        'only_matching': True,
    }, {
        'url': 'https://kaernten.orf.at/player/20200423/KGUMO',
        'only_matching': True,
    }, {
        'url': 'https://salzburg.orf.at/player/20200423/SGUM',
        'only_matching': True,
    }, {
        'url': 'https://tirol.orf.at/player/20200423/TGUMO',
        'only_matching': True,
    }, {
        'url': 'https://vorarlberg.orf.at/player/20200423/VGUM',
        'only_matching': True,
    }, {
        'url': 'https://oe3.orf.at/player/20200424/3WEK',
        'only_matching': True,
    }, {
        'url': 'http://oe1.orf.at/player/20170108/456544',
        'md5': '34d8a6e67ea888293741c86a099b745b',
        'info_dict': {
            'id': '2017-01-08_0759_tl_51_7DaysSun6_256141',
            'ext': 'mp3',
            'title': 'Morgenjournal',
            'duration': 609,
            'timestamp': 1483858796,
            'upload_date': '20170108',
        },
        'skip': 'Shows from ORF radios are only available for 7 days.'
    }]

    def _entries(self, data, station):
        _, loop_station, old_ie = self.STATION_INFO[station]
        for info in data['streams']:
            item_id = info.get('loopStreamId')
            if not item_id:
                continue
            video_id = item_id.replace('.mp3', '')
            yield {
                'id': video_id,
                'ext': 'mp3',
                'url': f'https://loopstream01.apa.at/?channel={loop_station}&id={item_id}',
                '_old_archive_ids': [make_archive_id(old_ie, video_id)],
                'title': data.get('title'),
                'description': clean_html(data.get('subtitle')),
                'duration': try_call(lambda: (info['end'] - info['start']) / 1000),
                'timestamp': int_or_none(info.get('start'), scale=1000),
                'series': data.get('programTitle'),
            }

    def _real_extract(self, url):
        station, station2, show_date, show_id = self._match_valid_url(url).group('station', 'station2', 'date', 'show')
        api_station, _, _ = self.STATION_INFO[station or station2]
        data = self._download_json(
            f'http://audioapi.orf.at/{api_station}/api/json/current/broadcast/{show_id}/{show_date}', show_id)

        return self.playlist_result(
            self._entries(data, station or station2), show_id, data.get('title'), clean_html(data.get('subtitle')))


class ORFPodcastIE(InfoExtractor):
    IE_NAME = 'orf:podcast'
    _STATION_RE = '|'.join(map(re.escape, (
        'bgl', 'fm4', 'ktn', 'noe', 'oe1', 'oe3',
        'ooe', 'sbg', 'stm', 'tir', 'tv', 'vbg', 'wie')))
    _VALID_URL = rf'https?://sound\.orf\.at/podcast/(?P<station>{_STATION_RE})/(?P<show>[\w-]+)/(?P<id>[\w-]+)'
    _TESTS = [{
        'url': 'https://sound.orf.at/podcast/oe3/fruehstueck-bei-mir/nicolas-stockhammer-15102023',
        'md5': '526a5700e03d271a1505386a8721ab9b',
        'info_dict': {
            'id': 'nicolas-stockhammer-15102023',
            'ext': 'mp3',
            'title': 'Nicolas Stockhammer (15.10.2023)',
            'duration': 3396.0,
            'series': 'Frühstück bei mir',
        },
        'skip': 'ORF podcasts are only available for a limited time'
    }]

    def _real_extract(self, url):
        station, show, show_id = self._match_valid_url(url).group('station', 'show', 'id')
        data = self._download_json(
            f'https://audioapi.orf.at/radiothek/api/2.0/podcast/{station}/{show}/{show_id}', show_id)

        return {
            'id': show_id,
            'ext': 'mp3',
            'vcodec': 'none',
            **traverse_obj(data, ('payload', {
                'url': ('enclosures', 0, 'url'),
                'ext': ('enclosures', 0, 'type', {mimetype2ext}),
                'title': 'title',
                'description': ('description', {clean_html}),
                'duration': ('duration', {functools.partial(float_or_none, scale=1000)}),
                'series': ('podcast', 'title'),
            })),
        }


class ORFIPTVIE(InfoExtractor):
    IE_NAME = 'orf:iptv'
    IE_DESC = 'iptv.ORF.at'
    _VALID_URL = r'https?://iptv\.orf\.at/(?:#/)?stories/(?P<id>\d+)'

    _TEST = {
        'url': 'http://iptv.orf.at/stories/2275236/',
        'md5': 'c8b22af4718a4b4af58342529453e3e5',
        'info_dict': {
            'id': '350612',
            'ext': 'flv',
            'title': 'Weitere Evakuierungen um Vulkan Calbuco',
            'description': 'md5:d689c959bdbcf04efeddedbf2299d633',
            'duration': 68.197,
            'thumbnail': r're:^https?://.*\.jpg$',
            'upload_date': '20150425',
        },
    }

    def _real_extract(self, url):
        story_id = self._match_id(url)

        webpage = self._download_webpage(
            'http://iptv.orf.at/stories/%s' % story_id, story_id)

        video_id = self._search_regex(
            r'data-video(?:id)?="(\d+)"', webpage, 'video id')

        data = self._download_json(
            'http://bits.orf.at/filehandler/static-api/json/current/data.json?file=%s' % video_id,
            video_id)[0]

        duration = float_or_none(data['duration'], 1000)

        video = data['sources']['default']
        load_balancer_url = video['loadBalancerUrl']
        abr = int_or_none(video.get('audioBitrate'))
        vbr = int_or_none(video.get('bitrate'))
        fps = int_or_none(video.get('videoFps'))
        width = int_or_none(video.get('videoWidth'))
        height = int_or_none(video.get('videoHeight'))
        thumbnail = video.get('preview')

        rendition = self._download_json(
            load_balancer_url, video_id, transform_source=strip_jsonp)

        f = {
            'abr': abr,
            'vbr': vbr,
            'fps': fps,
            'width': width,
            'height': height,
        }

        formats = []
        for format_id, format_url in rendition['redirect'].items():
            if format_id == 'rtmp':
                ff = f.copy()
                ff.update({
                    'url': format_url,
                    'format_id': format_id,
                })
                formats.append(ff)
            elif determine_ext(format_url) == 'f4m':
                formats.extend(self._extract_f4m_formats(
                    format_url, video_id, f4m_id=format_id))
            elif determine_ext(format_url) == 'm3u8':
                formats.extend(self._extract_m3u8_formats(
                    format_url, video_id, 'mp4', m3u8_id=format_id))
            else:
                continue

        title = remove_end(self._og_search_title(webpage), ' - iptv.ORF.at')
        description = self._og_search_description(webpage)
        upload_date = unified_strdate(self._html_search_meta(
            'dc.date', webpage, 'upload date'))

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'duration': duration,
            'thumbnail': thumbnail,
            'upload_date': upload_date,
            'formats': formats,
        }


class ORFFM4StoryIE(InfoExtractor):
    IE_NAME = 'orf:fm4:story'
    IE_DESC = 'fm4.orf.at stories'
    _VALID_URL = r'https?://fm4\.orf\.at/stories/(?P<id>\d+)'

    _TEST = {
        'url': 'http://fm4.orf.at/stories/2865738/',
        'playlist': [{
            'md5': 'e1c2c706c45c7b34cf478bbf409907ca',
            'info_dict': {
                'id': '547792',
                'ext': 'flv',
                'title': 'Manu Delago und Inner Tongue live',
                'description': 'Manu Delago und Inner Tongue haben bei der FM4 Soundpark Session live alles gegeben. Hier gibt es Fotos und die gesamte Session als Video.',
                'duration': 1748.52,
                'thumbnail': r're:^https?://.*\.jpg$',
                'upload_date': '20170913',
            },
        }, {
            'md5': 'c6dd2179731f86f4f55a7b49899d515f',
            'info_dict': {
                'id': '547798',
                'ext': 'flv',
                'title': 'Manu Delago und Inner Tongue live (2)',
                'duration': 1504.08,
                'thumbnail': r're:^https?://.*\.jpg$',
                'upload_date': '20170913',
                'description': 'Manu Delago und Inner Tongue haben bei der FM4 Soundpark Session live alles gegeben. Hier gibt es Fotos und die gesamte Session als Video.',
            },
        }],
    }

    def _real_extract(self, url):
        story_id = self._match_id(url)
        webpage = self._download_webpage(url, story_id)

        entries = []
        all_ids = orderedSet(re.findall(r'data-video(?:id)?="(\d+)"', webpage))
        for idx, video_id in enumerate(all_ids):
            data = self._download_json(
                'http://bits.orf.at/filehandler/static-api/json/current/data.json?file=%s' % video_id,
                video_id)[0]

            duration = float_or_none(data['duration'], 1000)

            video = data['sources']['q8c']
            load_balancer_url = video['loadBalancerUrl']
            abr = int_or_none(video.get('audioBitrate'))
            vbr = int_or_none(video.get('bitrate'))
            fps = int_or_none(video.get('videoFps'))
            width = int_or_none(video.get('videoWidth'))
            height = int_or_none(video.get('videoHeight'))
            thumbnail = video.get('preview')

            rendition = self._download_json(
                load_balancer_url, video_id, transform_source=strip_jsonp)

            f = {
                'abr': abr,
                'vbr': vbr,
                'fps': fps,
                'width': width,
                'height': height,
            }

            formats = []
            for format_id, format_url in rendition['redirect'].items():
                if format_id == 'rtmp':
                    ff = f.copy()
                    ff.update({
                        'url': format_url,
                        'format_id': format_id,
                    })
                    formats.append(ff)
                elif determine_ext(format_url) == 'f4m':
                    formats.extend(self._extract_f4m_formats(
                        format_url, video_id, f4m_id=format_id))
                elif determine_ext(format_url) == 'm3u8':
                    formats.extend(self._extract_m3u8_formats(
                        format_url, video_id, 'mp4', m3u8_id=format_id))
                else:
                    continue

            title = remove_end(self._og_search_title(webpage), ' - fm4.ORF.at')
            if idx >= 1:
                # Titles are duplicates, make them unique
                title += ' (' + str(idx + 1) + ')'
            description = self._og_search_description(webpage)
            upload_date = unified_strdate(self._html_search_meta(
                'dc.date', webpage, 'upload date'))

            entries.append({
                'id': video_id,
                'title': title,
                'description': description,
                'duration': duration,
                'thumbnail': thumbnail,
                'upload_date': upload_date,
                'formats': formats,
            })

        return self.playlist_result(entries)


class ORFONIE(InfoExtractor):
    IE_NAME = 'orf:on'
    _VALID_URL = r'https?://on\.orf\.at/video/(?P<id>\d+)'
    _TESTS = [{
        'url': 'https://on.orf.at/video/14210000/school-of-champions-48',
        'info_dict': {
            'id': '14210000',
            'ext': 'mp4',
            'duration': 2651.08,
            'thumbnail': 'https://api-tvthek.orf.at/assets/segments/0167/98/thumb_16697671_segments_highlight_teaser.jpeg',
            'title': 'School of Champions (4/8)',
            'description': 'md5:d09ad279fc2e8502611e7648484b6afd',
            'media_type': 'episode',
            'timestamp': 1706472362,
            'upload_date': '20240128',
            '_old_archive_ids': ['orftvthek 14210000'],
        }
    }, {
        'url': 'https://on.orf.at/video/3220355',
        'md5': 'f94d98e667cf9a3851317efb4e136662',
        'info_dict': {
            'id': '3220355',
            'ext': 'mp4',
            'duration': 445.04,
            'thumbnail': 'https://api-tvthek.orf.at/assets/segments/0002/60/thumb_159573_segments_highlight_teaser.png',
            'title': '50 Jahre Burgenland: Der Festumzug',
            'description': 'md5:1560bf855119544ee8c4fa5376a2a6b0',
            'media_type': 'episode',
            'timestamp': 52916400,
            'upload_date': '19710905',
            '_old_archive_ids': ['orftvthek 3220355'],
        }
    }]

    def _extract_video(self, video_id):
        encrypted_id = base64.b64encode(f'3dSlfek03nsLKdj4Jsd{video_id}'.encode()).decode()
        api_json = self._download_json(
            f'https://api-tvthek.orf.at/api/v4.3/public/episode/encrypted/{encrypted_id}', video_id)

        if traverse_obj(api_json, 'is_drm_protected'):
            self.report_drm(video_id)

        formats, subtitles = [], {}
        for manifest_type in traverse_obj(api_json, ('sources', {dict.keys}, ...)):
            for manifest_url in traverse_obj(api_json, ('sources', manifest_type, ..., 'src', {url_or_none})):
                if manifest_type == 'hls':
                    fmts, subs = self._extract_m3u8_formats_and_subtitles(
                        manifest_url, video_id, fatal=False, m3u8_id='hls')
                elif manifest_type == 'dash':
                    fmts, subs = self._extract_mpd_formats_and_subtitles(
                        manifest_url, video_id, fatal=False, mpd_id='dash')
                else:
                    continue
                formats.extend(fmts)
                self._merge_subtitles(subs, target=subtitles)

        for sub_url in traverse_obj(api_json, (
                '_embedded', 'subtitle',
                ('xml_url', 'sami_url', 'stl_url', 'ttml_url', 'srt_url', 'vtt_url'), {url_or_none})):
            self._merge_subtitles({'de': [{'url': sub_url}]}, target=subtitles)

        return {
            'id': video_id,
            'formats': formats,
            'subtitles': subtitles,
            '_old_archive_ids': [make_archive_id('ORFTVthek', video_id)],
            **traverse_obj(api_json, {
                'age_limit': ('age_classification', {parse_age_limit}),
                'duration': ('duration_second', {float_or_none}),
                'title': (('title', 'headline'), {str}),
                'description': (('description', 'teaser_text'), {str}),
                'media_type': ('video_type', {str}),
            }, get_all=False),
        }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        return {
            'id': video_id,
            'title': self._html_search_meta(['og:title', 'twitter:title'], webpage, default=None),
            'description': self._html_search_meta(
                ['description', 'og:description', 'twitter:description'], webpage, default=None),
            **self._search_json_ld(webpage, video_id, fatal=False),
            **self._extract_video(video_id),
        }

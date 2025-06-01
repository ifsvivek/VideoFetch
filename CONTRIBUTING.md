<div align="center">

# 🤝 Contributing to VideoFetch

**Thank you for your interest in contributing to VideoFetch!**

_We welcome contributions from developers of all skill levels and backgrounds._

</div>

---

## 📋 Table of Contents

-   [📖 Code of Conduct](#-code-of-conduct)
-   [🚀 Ways to Contribute](#-ways-to-contribute)
-   [⚡ Quick Start](#-quick-start)
-   [🛠️ Development Setup](#️-development-setup)
-   [📝 Code Guidelines](#-code-guidelines)
-   [🔍 Pull Request Process](#-pull-request-process)
-   [🐛 Reporting Issues](#-reporting-issues)
-   [💡 Feature Requests](#-feature-requests)
-   [📄 License](#-license)

---

## 📖 Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive environment for all contributors. By participating, you are expected to uphold this code.

**TL;DR**: Be respectful, be kind, be professional. 🤝

---

## 🚀 Ways to Contribute

There are many ways you can help improve VideoFetch:

### 🐛 Bug Reports

Found a bug? Help us squash it!

-   [Report a Bug](https://github.com/ifsvivek/VideoFetch/issues/new?template=bug_report.md)
-   Provide detailed steps to reproduce
-   Include system information and error messages

### 💡 Feature Requests

Have an idea for a new feature?

-   [Request a Feature](https://github.com/ifsvivek/VideoFetch/issues/new?template=feature_request.md)
-   Explain the use case and benefits
-   Discuss implementation approaches

### 🔧 Code Contributions

Ready to dive into the code?

-   Fix bugs and implement features
-   Improve documentation
-   Add tests and examples
-   Optimize performance

### 📚 Documentation

Help others understand the project:

-   Improve README and guides
-   Add code comments
-   Create tutorials and examples
-   Translate documentation

### 🧪 Testing

Ensure quality and reliability:

-   Test new features and bug fixes
-   Report compatibility issues
-   Improve test coverage

---

## ⚡ Quick Start

### For New Contributors

1. **🍴 Fork the Repository**

    ```bash
    # Click the "Fork" button on GitHub
    ```

2. **📥 Clone Your Fork**

    ```bash
    git clone https://github.com/yourusername/VideoFetch.git
    cd VideoFetch
    ```

3. **🌿 Create a Branch**

    ```bash
    git checkout -b feature/your-amazing-feature
    # or
    git checkout -b fix/bug-description
    ```

4. **✨ Make Your Changes**

    ```bash
    # Edit files, add features, fix bugs
    ```

5. **💾 Commit Your Changes**

    ```bash
    git add .
    git commit -m "Add amazing feature that does X"
    ```

6. **🚀 Push and Create PR**
    ```bash
    git push origin feature/your-amazing-feature
    # Then create a Pull Request on GitHub
    ```

---

## 🛠️ Development Setup

### Prerequisites

-   **Git** - Version control system
-   **Code Editor** - VS Code, Sublime Text, or your preferred editor
-   **Free Download Manager** - For testing the plugin

### Setup Instructions

1. **Fork and Clone**

    ```bash
    git clone https://github.com/ifsvivek/VideoFetch.git
    cd VideoFetch
    ```

2. **Explore the Structure**

    ```
    VideoFetch/
    ├── plugin/              # Main plugin files
    │   ├── manifest.json    # Plugin configuration
    │   ├── *.js            # JavaScript modules
    │   └── yt-dlp/         # Video extraction library
    ├── build/              # Build scripts
    ├── docs/               # Documentation
    └── .github/            # GitHub templates
    ```

3. **Make Your Changes**

    - Edit files in the `plugin/` directory
    - Follow the existing code structure
    - Test your changes thoroughly

4. **Build the Plugin** (if applicable)

    ```bash
    # On Unix/Linux/macOS
    cd build
    ./build-unix.sh

    # On Windows
    cd build
    build-windows.bat
    ```

5. **Test Your Changes**
    - Install the modified plugin in Free Download Manager
    - Test with various YouTube URLs
    - Verify functionality works as expected

---

## 📝 Code Guidelines

### General Principles

-   ✅ **Write Clean Code** - Clear, readable, and maintainable
-   ✅ **Follow Conventions** - Consistent with existing codebase
-   ✅ **Comment Wisely** - Explain _why_, not just _what_
-   ✅ **Test Thoroughly** - Ensure your changes work correctly

### JavaScript Style Guide

```javascript
// ✅ Good: Clear variable names and proper spacing
function downloadVideo(videoUrl, options) {
    const videoInfo = extractVideoInfo(videoUrl);

    if (!videoInfo.isValid) {
        throw new Error("Invalid video URL provided");
    }

    return processDownload(videoInfo, options);
}

// ❌ Avoid: Unclear names and poor formatting
function dl(u, o) {
    var i = ext(u);
    if (!i.ok) throw new Error("bad url");
    return proc(i, o);
}
```

### File Organization

-   **🗂️ Logical Structure** - Group related functionality
-   **📁 Consistent Naming** - Use descriptive file names
-   **🧹 Clean Dependencies** - Minimize external dependencies

### Documentation Standards

```javascript
/**
 * Downloads a YouTube video using the provided URL and options
 * @param {string} videoUrl - The YouTube video URL
 * @param {Object} options - Download configuration options
 * @param {string} options.quality - Video quality preference
 * @param {string} options.format - Output format (mp4, webm, etc.)
 * @returns {Promise<Object>} Download result object
 */
function downloadVideo(videoUrl, options) {
    // Implementation here
}
```

---

## 🔍 Pull Request Process

### Before Submitting

-   [ ] **✅ Code follows style guidelines**
-   [ ] **🧪 Changes have been tested**
-   [ ] **📝 Documentation is updated**
-   [ ] **🔄 No merge conflicts**
-   [ ] **📋 PR template is filled out**

### PR Requirements

1. **📊 Clear Description**

    - What changes were made?
    - Why were they necessary?
    - How should they be tested?

2. **🔗 Link Related Issues**

    ```markdown
    Fixes #123
    Closes #456
    Related to #789
    ```

3. **📷 Screenshots/GIFs** (if applicable)
    - Show UI changes
    - Demonstrate new features

### Review Process

1. **🔍 Automated Checks** - CI/CD pipeline runs
2. **👥 Code Review** - Maintainers review your code
3. **💬 Feedback** - Address any requested changes
4. **✅ Approval** - Once approved, your PR will be merged

---

## 🐛 Reporting Issues

### Before Creating an Issue

1. **🔍 Search Existing Issues** - Check if it's already reported
2. **📖 Check Documentation** - Review README and docs
3. **🧪 Test with Latest Version** - Ensure you're using the latest release

### Creating a Good Bug Report

Use our [Bug Report Template](https://github.com/ifsvivek/VideoFetch/issues/new?template=bug_report.md) and include:

-   **🎯 Clear Title** - Descriptive and specific
-   **📝 Detailed Description** - What happened vs. what was expected
-   **🔄 Reproduction Steps** - Step-by-step instructions
-   **🖥️ Environment Info** - OS, browser, FDM version
-   **📷 Screenshots/Logs** - Visual evidence or error logs

---

## 💡 Feature Requests

### Suggesting New Features

Use our [Feature Request Template](https://github.com/ifsvivek/VideoFetch/issues/new?template=feature_request.md) and include:

-   **🎯 Clear Use Case** - Why is this feature needed?
-   **📋 Detailed Description** - How should it work?
-   **🔄 Alternatives Considered** - Other approaches you've thought of
-   **📊 Implementation Ideas** - Technical suggestions (optional)

### Feature Development Process

1. **💬 Discussion** - Community feedback on the proposal
2. **✅ Approval** - Maintainers approve the feature
3. **🛠️ Implementation** - Development begins
4. **🧪 Testing** - Thorough testing and review
5. **🚀 Release** - Feature is included in next release

---

## 📄 License

By contributing to VideoFetch, you agree that your contributions will be licensed under the [MIT License](LICENSE).

This means:

-   ✅ Your code can be freely used and modified
-   ✅ Attribution will be maintained
-   ✅ No warranty or liability obligations

---

<div align="center">

**🙏 Thank You for Contributing!**

_Your contributions help make VideoFetch better for everyone._

**Questions?** Feel free to [open an issue](https://github.com/ifsvivek/VideoFetch/issues/new) or reach out to the maintainers.

---

_Made with ❤️ by the VideoFetch community_

</div>

<h1 align="center">Hi 👋, I'm Vikram</h1>
<h3 align="center">Video technologist · Encoding & streaming engineer · Rust & cloud infrastructure</h3>

<p align="center">I build video infrastructure in Rust — encoding optimizers, media metadata tooling, and the cloud pipelines that move it all.</p>

---

## 🚀 Featured Projects

### 🎬 [viser](https://github.com/vbasky/viser) — Video Encoding Optimizer
A multi-codec **convex-hull optimization pipeline** that computes per-content bitrate ladders from CRF sweep trial data. It combines shot detection and complexity analysis to drive per-title, per-shot, per-segment, and per-device encoding strategies — minimizing bitrate at any quality target.

> Ships BD-Rate computation, VMAF measurement, fixed-ladder comparison, chart rendering, and a browser-based comparison player.
>
> **15 workspace crates · H.264 / H.265 / AV1 · Rust**

### 🎧 [cathar](https://github.com/vbasky/cathar) — Audio Restoration Toolkit (Pure Rust)
An audio toolkit for any recording that **restores** (denoise, de-hum, de-click, de-clip, de-reverb), **enhances** (de-ess, breath removal, voice isolation, bandwidth extension), and **levels** (LUFS + peak normalisation) — writing a clean 32-bit float WAV. Works on standalone audio (WAV, MP3, FLAC, OGG, M4A) or the audio track inside a video; video is never required.

> No ffmpeg, no C/C++, no system libraries — decoding via `symphonia`, FFT via `realfft`/`rustfft`. Every effect is a plain function over `&[f32]`, so the pipeline drops straight into any Rust program.
>
> **Pure Rust · single `cargo build` · MSRV 1.85 / edition 2024**

### 🖼️ [eligo](https://github.com/vbasky/eligo) — Best-of-N Image Selection (Pure Rust)
Image generators are random — eligo automates picking the best output. Give it a prompt and it **generates** `n` candidates (a pluggable `Backend`), **scores** each against the prompt (a pluggable `Scorer`), and **selects** the highest-scoring one. The smallest honest **agentic** loop: a numeric reward drives a decision.

> Ships a Stable Diffusion backend on ONNX Runtime, a CLIP prompt-alignment scorer, no-reference quality scoring, and image-similarity search — with a bounded single re-roll of the worst candidate.
>
> **Pure Rust · ONNX Runtime · CLIP · Stable Diffusion**

### 🔎 [revelo](https://github.com/vbasky/revelo) — Pure-Rust MediaInfoLib Port
A safe, fast port of MediaInfoLib that reads technical and tag metadata from **177+ audio, video, image, and container formats**. A drop-in `libmediainfo` replacement (C ABI + CLI), differential-tested byte-for-byte against the MediaInfo oracle.

> AAC · AC-3 · AVI · AV1 · BPG · CineForm · DTS · DV · FLAC · H.263 · JPEG · MPEG · MP4/MOV · Matroska · MPEG-PS/TS · Ogg · Opus · PNG · ProRes · VC-1 · VP8/9 · WebP · WAV · and more
>
> 🍺 `brew install vbasky/revelo/revelo`

### 🗄️ [somnia](https://github.com/vbasky/somnia) — Type-safe SurrealDB ORM for Rust
A typed query builder, a `#[derive(SurrealRecord)]` macro, schema generation, and Diesel-style migrations — bringing compile-time safety to SurrealDB.

> 🍺 `brew install vbasky/somnia/somnia`

### 🎨 [sublime-vscode-plus](https://github.com/vbasky/sublime-vscode-plus) — VS Code Colour Scheme for Sublime Text
Brings VS Code's **Dark+** and **Light+** syntax highlighting to Sublime Text. Installable via Package Control and tested across PHP, JavaScript/Vue, Python, HTML/Blade, CSS/Sass/SCSS/Less, JSON, XML, Markdown, and YAML.

> ⭐ **45 stars** — my most-starred project

### 📓 [patina](https://github.com/vbasky/patina) — Rust-native Interactive Notebook
A Rust-native interactive notebook with kernel support for **Rust**, **Python**, and **JavaScript**. The entire stack — web server, kernels, wire protocol, and JavaScript engine — is written in Rust. No Jupyter, no external kernel plumbing.

> Rust (evcxr) · Python (pyo3/CPython) · JavaScript (boa) · React UI · Axum

### ⚡ [azure-rust-functions](https://github.com/vbasky/azure-rust-functions) — Azure Functions in Rust
A working pattern for running Azure Functions on the Rust custom-handler runtime.

---

## 💼 Professional experience

| Area | Technologies |
|------|-------------|
| **Video streaming** | DASH, HLS, LL-HLS, CMAF, MPEG-TS, MP4 fragmented, manifest generation |
| **Cloud media (AWS)** | Elemental MediaConvert, MediaLive, MediaPackage, MediaTailor, CloudFront |
| **Cloud media (Azure)** | Azure AI, AKS, Azure Functions, App Service, Event Hubs, Service Bus, Storage, Cosmos DB |
| **Video encoding** | H.264/AVC, H.265/HEVC, AV1, VP9, per-title optimization, quality metrics (VMAF, PSNR, SSIM, BD-Rate) |
| **Infrastructure** | Docker, Kubernetes, Terraform, CI/CD, monitoring, cost optimization |
| **Software** | Rust, C#/.NET, Java, TypeScript, JavaScript, Laravel |

---

<h3 align="left">Connect with me</h3>
<p align="left">
<a href="https://twitter.com/vikrambhaskar" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="vikrambhaskar" height="30" width="40" /></a>
<a href="https://au.linkedin.com/in/vbasky" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="vbasky" height="30" width="40" /></a>
</p>

<p align="left"> <a href="https://twitter.com/vikrambhaskar" target="blank"><img src="https://img.shields.io/twitter/follow/vikrambhaskar?logo=twitter&style=for-the-badge" alt="vikrambhaskar" /></a> </p>

### Languages

![Rust](https://img.shields.io/badge/-Rust-AA2704?logo=Rust&logoColor=white&style=flat)
![C#](https://img.shields.io/badge/-C%23-%23239120?logo=c-sharp&logoColor=white&style=flat)
![Java](https://img.shields.io/badge/-Java-ED8B00?logo=openjdk&logoColor=white&style=flat)
![TypeScript](https://img.shields.io/badge/Typescript-%23007ACC.svg?&logo=typescript&logoColor=white&style=flat)
![JavaScript](https://img.shields.io/badge/-Javascript-f7df1e?logo=Javascript&logoColor=white&style=flat)

### Cloud & Infrastructure

![AWS](https://img.shields.io/badge/-AWS-232F3E?logo=amazon-aws&logoColor=white&style=flat)
![AWS Elemental](https://img.shields.io/badge/-AWS%20Elemental-FF9900?logo=amazon-aws&logoColor=white&style=flat)
![Azure](https://img.shields.io/badge/-Azure-0089D6?logo=microsoft-azure&logoColor=white&style=flat)
![Azure AI](https://img.shields.io/badge/-Azure%20AI-0078D4?logo=microsoft-azure&logoColor=white&style=flat)
![AKS](https://img.shields.io/badge/-AKS-326CE5?logo=kubernetes&logoColor=white&style=flat)
![Docker](https://img.shields.io/badge/-Docker-0DB7ED?logo=Docker&logoColor=white&style=flat)
![Kubernetes](https://img.shields.io/badge/-Kubernetes-326CE5?logo=kubernetes&logoColor=white&style=flat)
![Terraform](https://img.shields.io/badge/-Terraform-844FBA?logo=terraform&logoColor=white&style=flat)

### Video & Media

![H.264](https://img.shields.io/badge/-H.264-00599C?style=flat)
![H.265](https://img.shields.io/badge/-H.265-00599C?style=flat)
![AV1](https://img.shields.io/badge/-AV1-00599C?style=flat)
![VMAF](https://img.shields.io/badge/-VMAF-00ADD8?style=flat)
![DASH](https://img.shields.io/badge/-DASH-00A98F?style=flat)
![HLS](https://img.shields.io/badge/-HLS-00A98F?style=flat)

### Frameworks & Tools

![.NET](https://img.shields.io/badge/-.NET-413CFB?logo=.net&logoColor=white&style=flat)
![Laravel](https://img.shields.io/badge/-Laravel-F55247?logo=Laravel&logoColor=white&style=flat)
![React](https://img.shields.io/badge/-React-61DBFB?logo=react&logoColor=white&style=flat)
![Redis](https://img.shields.io/badge/-Redis-D82C20?logo=Redis&logoColor=white&style=flat)
![Nginx](https://img.shields.io/badge/Nginx-%23009639.svg?&logo=nginx&logoColor=white&style=flat)

### Databases

![Mysql](https://img.shields.io/badge/-Mysql-00758F?logo=Mysql&logoColor=white&style=flat)
![SqlServer](https://img.shields.io/badge/-SqlServer-B71D1C?logo=microsoft-sql-server&logoColor=white&style=flat)
![SurrealDB](https://img.shields.io/badge/SurrealDB-FF00A0?style=flat&logo=data:image/svg%2Bxml;base64,PHN2ZyBmaWxsPSIjZmZmZmZmIiByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU+U3VycmVhbERCPC90aXRsZT48cGF0aCBkPSJtMTIgNi4zMTQgNS43MTQgMy4xNjV2LTEuMjdMMTIgNS4wNTRjLS44NS40Ny00Ljk1NyAyLjc0LTUuNzE0IDMuMTU3LjcwMy4zOSA4LjA4NSA0LjQ2NyAxMi41NzIgNi45NDZ2MS4yNjRMMTIgMjAuMjA5Yy0xLjcxLS45NDMtNS4xNS0yLjg0NC02Ljg1OC0zLjc5di0zLjc4OEwxMiAxNi40MmwxLjE0NC0uNjMyLTkuMTQ2LTUuMDV2Ni4zMTZMMTIgMjEuNDcybDgtNC40MnYtMi41MjZMOC41NyA4LjIxWm0tOC4wMDIuNjMydjIuNTI4bDExLjQyOCA2LjMxNi0zLjQyOCAxLjg5Ni01LjcxNC0zLjE2NXYxLjI3bDUuNzE0IDMuMTU2Yy44NS0uNDcgNC45NTctMi43NCA1LjcxNC0zLjE1Ny0uNzAzLS4zOS04LjA4My00LjQ2Ny0xMi41Ny02Ljk0OFY3LjU3OEwxMiAzLjc4OWMxLjcwNy45NDUgNS4xNDggMi44NDYgNi44NTggMy43ODl2My43ODlMMTIgNy41NzdsLTEuMTQ0LjYzM0wyMCAxMy4yNjNWNi45NDZMMTIgMi41MjZjLS43OTEuNDM4LTcuNDE2IDQuMS04LjAwMiA0LjQyek0xMiAwIDEuNzEzIDUuNjg1djEyLjYzTDEyIDI0bDEwLjI4Ny01LjY4MlY1LjY4NVptOS4xNCAxNy42ODNMMTIgMjIuNzM2bC05LjE0My01LjA1M1Y2LjMxN0wxMiAxLjI2NGw5LjE0MyA1LjA1M3oiLz48L3N2Zz4=)

### Platforms

![Linux](https://img.shields.io/badge/-Linux-E95420?logo=Linux&logoColor=white&style=flat)
![macOS](https://img.shields.io/badge/-macOS-A2AAAD?logo=Apple&logoColor=white&style=flat)
![Windows](https://img.shields.io/badge/-Windows-357EC7?logo=Windows&logoColor=white&style=flat)

---

<p>&nbsp;<img align="center" src="https://github-readme-stats.vercel.app/api?username=vbasky&show_icons=true&locale=en" alt="vbasky" /></p>
<p><img align="center" src="https://github-readme-streak-stats.herokuapp.com/?user=vbasky&" alt="vbasky" /></p>

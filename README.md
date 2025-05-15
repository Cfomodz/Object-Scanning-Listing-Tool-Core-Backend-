<div align="center">

# Object Scanning & Listing Tool (Core Backend)
![GitHub License](https://img.shields.io/github/license/Cfomodz/PCGS-slab-picture-to-listing-tool)
![GitHub Sponsors](https://img.shields.io/github/sponsors/Cfomodz)
![Discord](https://img.shields.io/discord/425182625032962049)

<img src="https://github.com/user-attachments/assets/26fa2e62-64ed-43de-b0df-4465947d512e" alt="Object Scan Tool" width="400"/>

### ✨ From images to listings & labels, for any collectible ✨
**Scan, identify, and list any item type with a modular, plugin-based backend**
</div>

---

## 🚀 Quick Start

1. **Install**
   ```bash
   git clone https://github.com/Cfomodz/Object-Scanning-Listing-Tool-Core-Backend-.git
   cd Object-Scanning-Listing-Tool-Core-Backend
   pip install -r requirements.txt
   ```

2. **Configure**
   - Copy `.env.example` to `.env` and set any global environment variables.
   - Each plugin may have its own `.env` for item-type-specific settings.

3. **Run**
   ```bash
   python main.py <item_type> [args...]
   # Example: python main.py coin --images ./images
   ```

---

## 🧩 Architecture Overview

- **Core Backend**: Provides abstract base classes, barcode/image utilities, listing/box/order management, and a plugin registry.
- **Plugin System**: Each item type (coins, cards, comics, etc.) is implemented as a plugin, with its own scanner, listing builder, and label writer.
- **Stateless API**: Designed for integration with any frontend or automation pipeline.
- **Extensible**: Add new item types by creating a new plugin directory and implementing the required interfaces.

---

## 🔑 Key Features

- 📦 Modular box/order management for any item type
- 🖨️ Label generation and printing (PDF, QR/barcode, etc.)
- 📷 Barcode and image-based identification utilities
- 🧩 Plugin discovery and dynamic dispatch
- 💾 Caching and persistence utilities
- 🧪 Full test suite for core and plugins

---

## ⚙️ Setup & Configuration

- **Global settings**: Place in `.env` at the project root.
- **Plugin settings**: Each plugin can have its own `.env` (see plugin's `.env.example`).
- **Dependencies**: See `requirements.txt` for required Python packages.

---

## 🛠️ Extending the System

1. **Create a new plugin**:
   - Add a directory under `plugins/` (e.g., `plugins/cards/`).
   - Implement `ItemScanner`, `ListingBuilder`, and (optionally) `LabelWriter` subclasses.
   - Register your plugin in its `__init__.py`.

2. **Add tests**:
   - Place plugin-specific tests in `plugins/<your_plugin>/tests/`.
   - Core tests live in the `tests/` directory.

3. **Integrate with the API or CLI**:
   - The core system will discover and use your plugin automatically.

---

## 📚 Example Workflow

1. **Capture images** of your items (any type) using your preferred frontend or camera tool.
2. **Send images to the backend** via API or CLI, specifying the item type.
3. **Backend identifies, builds listings, and generates labels** using the appropriate plugin.
4. **Export listings** as JSON, send to an external API, or print labels as needed.

---

## 📜 License
LGPL-2.1

💌 Questions? Open an issue or join the Discord!

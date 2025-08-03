# 🎯 VS Code Workspace Configuration

## ✅ **VS Code Setup Complete!**

Your VS Code workspace has been configured with the new organized file structure and enhanced development tools.

## 🛠️ **VS Code Tasks Available**

Access these tasks via `Ctrl+Shift+P` → "Tasks: Run Task":

### 🚀 **Development Tasks**

- **Start Backend Server** - Runs FastAPI server from `backend/main.py`
- **Setup Development Environment** - Runs `./scripts/setup.sh`
- **Create Sample Data** - Populates database with test data
- **Open Frontend** - Opens `frontend/index.html` in browser

### 🐳 **Docker Tasks**

- **Start Docker Services** - Runs `./scripts/docker-start.sh`
- **Stop Docker Services** - Runs `./scripts/docker-stop.sh`

## 🐛 **Debug Configurations**

Access via `F5` or Debug panel:

### **Debug Backend Server**

- Launches FastAPI server with debugger attached
- Breakpoints work in all backend Python files
- Environment configured for `backend/` directory

### **Debug Sample Data Creation**

- Debug the sample data generation script
- Useful for testing database operations

## ⚙️ **Workspace Settings**

### **Python Configuration**

- ✅ Virtual environment auto-detection (`.venv`)
- ✅ Python path includes `backend/` and `scripts/`
- ✅ Linting with Flake8
- ✅ Formatting with Black
- ✅ Auto-organize imports on save

### **File Management**

- ✅ Hide Python cache files (`__pycache__`, `*.pyc`)
- ✅ Exclude database files from search
- ✅ Show virtual environment folder
- ✅ File associations for Docker, YAML, shell scripts

### **Editor Enhancements**

- ✅ Format on save enabled
- ✅ 88-character ruler for Python (Black standard)
- ✅ Auto-organize imports
- ✅ Proper terminal working directory

## 📦 **Recommended Extensions**

Install these extensions for the best development experience:

### **Python Development**

- `ms-python.python` - Python language support
- `ms-python.debugpy` - Python debugger
- `ms-python.flake8` - Python linting
- `ms-python.black-formatter` - Code formatting

### **Web Development**

- `ms-vscode.live-server` - Live server for frontend
- `esbenp.prettier-vscode` - Code formatting
- `ms-vscode.vscode-eslint` - JavaScript linting

### **DevOps & Docker**

- `ms-vscode.vscode-docker` - Docker support
- `redhat.vscode-yaml` - YAML language support

### **General Productivity**

- `formulahendry.auto-rename-tag` - HTML tag auto-rename
- `ms-vscode.vscode-json` - Enhanced JSON support

## 🚀 **Quick Start Guide**

### 1. **Setup Development Environment**

```bash
# Run task: "Setup Development Environment"
# Or manually: ./scripts/setup.sh
```

### 2. **Start Backend Server**

```bash
# Run task: "Start Backend Server"
# Or press F5 to debug
```

### 3. **Open Frontend**

```bash
# Run task: "Open Frontend"
# Or manually open frontend/index.html
```

### 4. **Alternative: Use Docker**

```bash
# Run task: "Start Docker Services"
# Access at http://localhost:3000
```

## 📁 **File Navigation**

With the organized structure:

```
StackHealth/
├── backend/          # Python FastAPI backend
├── frontend/         # HTML/CSS/JS frontend
├── scripts/          # Development scripts
├── docs/            # Documentation
├── data/            # Database storage
└── .vscode/         # VS Code configuration
```

## 🎯 **Development Workflow**

### **Traditional Development**

1. Run task: "Setup Development Environment"
2. Run task: "Start Backend Server"
3. Run task: "Open Frontend"
4. Run task: "Create Sample Data" (optional)

### **Docker Development**

1. Run task: "Start Docker Services"
2. Access http://localhost:3000 (frontend)
3. Access http://localhost:8000/docs (API)

### **Debugging**

1. Press `F5` or use Debug panel
2. Select "Debug Backend Server"
3. Set breakpoints in Python files
4. Debug with full variable inspection

## ✨ **Features**

### **Auto-Detection**

- ✅ Python virtual environment automatically activated
- ✅ Correct Python interpreter selected
- ✅ Environment paths configured

### **Code Quality**

- ✅ Linting on save with Flake8
- ✅ Formatting on save with Black
- ✅ Import organization
- ✅ Type checking support

### **Productivity**

- ✅ Integrated terminal with correct working directory
- ✅ File exclusions for cleaner workspace
- ✅ Docker and YAML syntax highlighting
- ✅ Live reload for frontend development

## 🎉 **Ready to Code!**

Your VS Code workspace is now perfectly configured for:

- ✅ **Python backend development** with debugging
- ✅ **Frontend development** with live reload
- ✅ **Docker development** with one-click deployment
- ✅ **Professional code quality** with linting and formatting
- ✅ **Efficient workflow** with organized tasks and shortcuts

Start developing with `F5` or run any task with `Ctrl+Shift+P` → "Tasks: Run Task"!

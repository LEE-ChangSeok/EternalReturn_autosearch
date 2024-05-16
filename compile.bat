pushd "%~dp0"

:: optimized판 컴파일
:: python -O -m PyInstaller main.spec

:: debug판 컴파일
:: python -d -m PyInstaller main.spec
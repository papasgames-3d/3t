@echo off  

REM Dòng này di chuyển vào thư mục chứa file .bat  
cd /d %~dp0  

REM Gọi script Python  
python add_new_game.py  

pause  
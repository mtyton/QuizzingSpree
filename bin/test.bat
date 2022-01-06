@echo off

CALL env.bat

set "DATABASE_URI=mysql+mysqlconnector://<your_username>:<your_password>@127.0.0.1/test_quizzing_spree"

pytest $*

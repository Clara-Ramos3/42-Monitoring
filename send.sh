#!bash

curl -X POST \
     -F "username=$USER" \
     -F "message1=@days/26.txt" \
     -F "message2=@days/26.txt" \
     https://pzau.pythonanywhere.com/register

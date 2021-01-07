CONFIGURAÇÕES

## TOOLS
sudo apt-get install git python3 python3-pip python3-venv -y

## GIT
git clone https://github.com/carlos-ft/rhavPad.git
cd rhavPad

## REDIS
sudo apt-get install redis-server -y
sudo systemctl start redis-server
sudo systemctl enable redis-server
edis-cli ping

## PYTHON
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## START
gunicorn --bind 0.0.0.0:5000 wsgi:app


deactivate
sudo nano /etc/systemd/system/rhavpad.service

--
[Unit]
Description=Gunicorn instance to serve rhavpad
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/rhavpad
Environment="PATH=/home/rhavpad/venv/bin"
ExecStart=/home/rhavpad/venv/bin/gunicorn --workers 3 --bind unix:rhavpad.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
--

sudo systemctl start rhavpad
sudo systemctl enable rhavpad

sudo nano /etc/nginx/sites-available/rhavpad

--
server {
    listen 80;
    server_name rhavpad.rhavena.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/rhavpad/rhavpad.sock;
    }
}
--

sudo ln -s /etc/nginx/sites-available/rhavpad /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

sudo docker-compose build --no-cache
sudo docker-compose up -d
sudo docker-compose ps
sudo docker-compose logs -f
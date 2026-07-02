# Project Development Steps (core features wo cloud infra configs)

```
/nve-rsync-host-monitor/         # root project directory
│
├── app/
│   ├── templates/               #
│   │   ├── index.html           #
│   │   └── chart.html           #
│   │
│   ├── __init__.py              #
│   ├── config.py                #
│   ├── crud.py                  #
│   ├── database.py              #
│   ├── main.py                  #
│   ├── models.py                #
│   └── schemas.py               #
│
├── configs/
│   ├── systemd/                 # 
│   │   └── monitoring.service   #
│   └── monitoring.conf          #
│
├── data/                        #
│   └── monitoring.db            #
│
├── infra/                       #
│   └── docker/                  #
│       ├── Dockerfile           #
│       └── docker-compose.yaml  #
│
├── logs/                        # 
│   └── sync.log                 # 
│
├── scripts/
│   ├── deploy_install.sh        # 
│   ├── deploy_uninstall.sh      # 
│   ├── run.sh                   # 
│   └── backupDB.sh              # 
│
├── static/                      # 
│   ├── css/                     # 
│   │   └── style.css
│   └── js/                      # 
│       └── main.js
│
├── venv/                        # 
│
├── .gitignore                   # 
├── LICENSE                      # 
├── README_structure.md          # 
├── README.md                    # 
└── requirements.txt             # 

```

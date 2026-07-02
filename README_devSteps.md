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
│   ├── config.py                # step-001 <
│   ├── crud.py                  # step-005 <
│   ├── database.py              # step-002 <
│   ├── main.py                  # step-006 <
│   ├── models.py                # step-003 <
│   └── schemas.py               # step-004 <
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
└── requirements.txt             # step-007 <

```

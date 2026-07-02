# Project Development Steps (core features wo cloud infra configs)

```
/nve-rsync-host-monitor/                    # root project directory
│
├── app/
│   ├── templates/                          #
│   │   ├── index.html                      #
│   │   └── chart.html                      #
│   │
│   ├── __init__.py                         #
│   ├── config.py                           # step-001
│   ├── crud.py                             # step-005
│   ├── database.py                         # step-002
│   ├── main.py                             # step-006
│   ├── models.py                           # step-003
│   └── schemas.py                          # step-004
│
├── configs/
│   ├── systemd/                            #
│   │   └── nve-rsync-monitor-prod.service  # step-008.1 <
│   └── monitor.conf                        # <
│
├── data/
│   ├── backups/                            # step-012.0 <
│   │   └── monitorDB_20260702_1720.tar.gz  # < step-013
│   └── monitor.db                          # <
│
├── infra/                                  #
│   └── docker/                             #
│       ├── Dockerfile                      #
│       └── docker-compose.yaml             #
│
├── logs/                                   #
│   ├── backup.log.example                  # step-012.2 <
│   ├── service_err.log.example             # step-008.2 <
│   ├── service_out.log.example             # step-008.3 <
│   └── sync.log                            #
│
├── scripts/
│   ├── backupDB.sh                         # step-012.1 <
│   ├── deploy_install.sh                   # step-010 <
│   ├── deploy_uninstall.sh                 # step-011 <
│   └── run.sh                              # step-009 <
│
├── static/                                 #
│   ├── css/                                #
│   │   └── style.css                       #
│   └── js/                                 #
│       └── main.js                         #
│
├── venv/                                   #
│
├── .gitignore                              #
├── LICENSE                                 #
├── README_structure.md                     #
├── README.md                               #
└── requirements.txt                        # step-007

```

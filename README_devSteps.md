# Project Development Steps (core features wo cloud infra configs)

```
/nve-rsync-host-monitor/                    # root project directory
│
├── .github/                                # step-015
│   └── workflows/                          # step-016
│       └── deploy.yaml                     # step-017,019 <
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
│   ├── main.py                             # step-006,018
│   ├── models.py                           # step-003
│   └── schemas.py                          # step-004
│
├── configs/
│   ├── systemd/                            #
│   │   └── nve-rsync-monitor-prod.service  # step-008.1
│   └── monitor.conf                        #
│
├── data/
│   ├── backups/                            # step-012.0
│   │   └── monitorDB_20260702_1720.tar.gz  # step-013
│   └── monitor.db                          #
│
├── infra/                                  #
│   └── docker/                             #
│       ├── Dockerfile                      #
│       └── docker-compose.yaml             #
│
├── logs/ 
│   ├── examples/                           #
│   │   ├── backup.log.example              # step-012.2
│   │   ├── service_err.log.example         # step-008.2
│   │   └── service_out.log.example         # step-008.3
│   └── sync.log                            #
│
├── scripts/
│   ├── db_backup.sh                        # step-012.1
│   ├── db_restore.sh                       # step-014
│   ├── deploy_install.sh                   # step-010
│   ├── deploy_uninstall.sh                 # step-011
│   └── run.sh                              # step-009
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
├── README_devSteps.md                      #
├── README_structure.md                     #
├── README.md                               # <
└── requirements.txt                        # step-007

```

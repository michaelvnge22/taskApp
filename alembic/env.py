from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

import os
import sys

# --- IMPORTANT ---
# Ajoute le chemin du projet pour que Alembic trouve app/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Maintenant on peut importer les modèles et la Base SQLAlchemy
from app.database import Base
from app import models  # noqa: F401  (important pour que Alembic détecte les modèles)

# Charge la configuration Alembic
config = context.config

# Configure le logger Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Cible des métadonnées pour l’autogénération
target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# FONCTIONS ALEMBIC
# ---------------------------------------------------------------------------

def run_migrations_offline():
    """Exécute les migrations en mode 'offline'."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # détecte changements de type
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Exécute les migrations en mode 'online'."""
    configuration = config.get_section(config.config_ini_section)

    # On lit l’URL de la BDD depuis alembic.ini
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # détecte changements de colonnes
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

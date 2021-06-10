# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from dependency_injector import containers, providers

from src.domain.dto.playerdto import PlayerInternal


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    internal_model = providers.Factory(PlayerInternal, url_env=config.url_env, routes=config.routes)

# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from dependency_injector import containers, providers

from domain.dto.playerdto import PlayerInternalModel


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    internal_model = providers.Factory(
        PlayerInternalModel,
        url_env=config.url_env,
        routes=config.routes,
    )
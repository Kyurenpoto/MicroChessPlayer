# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import pytest
from dependency_injector import providers
from src.config import Container
from src.converter.responseconverter import GameResponseToDTO
from src.framework.dto.playerdto import PlayerAIInfo, PlayerAPIInfo, PlayerGameRequest
from src.entity.movement import FEN
from src.framework.intent.gameintent import GameIntent
from src.usecase.game import FakeGameFactory


@pytest.mark.asyncio
async def test_game_intent(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="game", method="post"))

    assert (
        await GameIntent.from_usecase_factory(FakeGameFactory()).executed(
            PlayerGameRequest(white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"))
        )
        == GameResponseToDTO([FEN.starting()], [], "1-0").convert()
    )

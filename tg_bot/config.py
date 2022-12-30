from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    # admin_ids: list[int]
    use_news: bool
    token_news: str
    token_nasa: str
    use_nasa: bool
    summaryzer_on: bool


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None):
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            # admin_ids=list(map(int, env.list("ADMINS"))),
            use_news=env.bool("USE_NEWS"),
            token_news=env.str('TOKEN_NEWS'),
            token_nasa=env.str('TOKEN_NASA'),
            use_nasa=env.bool("USE_NASA"),
            summaryzer_on=env.bool("SUMMARYZER_ON")
        )
    )

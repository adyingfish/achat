# strategies/strategy_factory.py
from . import (
    NormalOrderStrategy,
    FlashSaleStrategy,
    GroupBuyStrategy,
    GroupBuyStrategy
)


class WorkflowStrategyFactory:
    @staticmethod
    def create_strategy(chat_type: str) -> ChatStrategy:
        strategies = {
            "normal_chat": NormalChatStrategy(),
            "web_search": ChatStrategy(),
            "regenerate": ChatStrategy(),
            "edit_resend": ChatStrategy()
        }
        if chat_type not in strategies:
            raise HTTPException(400, "不支持的订单类型")

        return strategies[chat_type]
# type: ignore

from aredis_om import (
    EmbeddedJsonModel,
    Field,
    JsonModel
)
class ItemMetadata(EmbeddedJsonModel):
    title: str = Field(index=True, full_text_search=True)
    article_type: str = Field(index=True)
    application: str = Field(index=True)
    text: str = str


class ItemEntity(JsonModel):
    item_id: int = Field(index=True)
    item_metadata: ItemMetadata

import uuid
from pydantic import BaseModel, Field


class Minutes(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str
    abstract_summary: str
    key_points: str
    # sentiment: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Conference Room",
                "abstract_summary": "Leonardo DiCaprio, speaking at the United Nations, emphasizes the urgent need to address climate change. He highlights the increasing evidence of climate events, such as droughts, ocean acidification, and melting ice sheets, and emphasizes that this is not rhetoric but fact. DiCaprio calls for decisive action from industries and governments worldwide, including putting a price on carbon emissions and ending subsidies for fossil fuel companies. He argues that renewable energy is not only achievable but also good economic policy. DiCaprio urges leaders to recognize that clean air and a livable climate are human rights and that solving the climate crisis is a matter of survival. He concludes by urging delegates to face this challenge with courage and honesty.",
                
                "action_items": "There are no specific action items or tasks mentioned in this text. The speaker is urging the audience, which includes government leaders and delegates, to take decisive, large-scale action to address the climate crisis. However, there are no specific actions or assignments mentioned.",
                
                "key_points": "- The speaker is a concerned citizen who participated in a climate change march in New York.\n- Climate change is a real and urgent crisis, supported by scientific evidence.\n- Climate change is causing droughts, ocean acidification, extreme weather events, and melting ice sheets.\n- The US military recognizes climate change as a significant security threat.\n- The speaker calls for decisive, large-scale action from industries and governments worldwide.\n- Carbon emissions should be priced and government subsidies for fossil fuel companies should be eliminated.\n- Renewable energy is economically viable and should be pursued.\n- Climate change is not a partisan issue but a human one.\n- Clean air and a livable climate are human rights.\n- Solving the climate crisis is a matter of survival.\n- The speaker urges world leaders to face the challenge with courage and honesty."
                
                # "sentiment": "The sentiment of the text is generally positive. The speaker expresses gratitude and honor for being present and acknowledges the urgency of the climate crisis. The language used is passionate and emotive, conveying concern and a sense of urgency. The speaker emphasizes the need for decisive action by industries and governments worldwide. The text also highlights the potential economic benefits of renewable energy and calls for an end to government subsidies for polluting industries. The overall tone is one of urgency, hope, and a plea for action.",
            }
        }

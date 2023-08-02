import os
import openai
openai.organization = "org-3oHj3jV2OQX6QX6QX6QX6QX6"
openai.api_key = os.getenv("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")
openai.Model.list()
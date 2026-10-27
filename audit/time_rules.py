"""Conservative hold rules for source claims that can age without a stated date."""
import re

def temporal_hold(prompt,topic):
    dated=bool(re.search(r'\b(?:as of|by|in|during|between|from|until)\s+(?:the\s+)?(?:1[0-9]{3}|20[0-9]{2})\b',prompt,re.I))
    reasons=[]
    if not dated:
        if re.search(r'\b(?:most|largest|smallest|biggest|longest|shortest|highest|lowest|fastest|slowest|oldest|youngest|richest|best|leading|latest|current|record[- ]holding|world record)\b',prompt,re.I): reasons.append('undated_superlative_or_record_requires_editorial_review')
        if topic!='19' and re.search(r'\bhow (?:many|much|old)\b.*\b(?:is|are|has|have|does|do)\b|\bhow (?:old|many) (?:is|are|has|have)\b',prompt,re.I): reasons.append('undated_present_quantity_requires_editorial_review')
        if re.search(r'\b(?:CEO|chief executive|net worth|married to|lives in|belongs to which party|population of)\b',prompt,re.I): reasons.append('undated_changing_personal_or_demographic_fact')
    return reasons

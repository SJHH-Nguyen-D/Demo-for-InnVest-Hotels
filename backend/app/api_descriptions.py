main_description = """
Apogee API. With the multiple tools available below, you can do the following tasks:
1. Ingestion of single or multiple website data.
2. Crawling through the given websites and their domains to extract further data.
3. Upload individual or multiple documents to storage and extract their metadata.
4. Get recommendations on queries you might have in regards to stored documents and webpages.
5. Deploy bots for chatting and getting automated information tailored to your desires.

If there is some functionality that you think should be present within the currently available processes, please
let us know by going to our [website](https://1000ml.io/) and contact us there!
"""

bots_sdks_deploys = """
The following routes are all related to each other via functionality, and through the database. A deployment is
considered to be a particular grouping of SDKs (not yet implemented) and Bots that are designed to share a similar
overarching purpose. The bots are meant to hold information and functionality that allow for interaction with a user.
Usually, this would be something like a chatbot. Each chatbot, will contain a particular Conversation Flow, which holds
onto the text, questions, answers and responses that the bot knows how to respond with. The Questions that a chatbot
need to know to ask are held within Questions, which come with a list of possible responses. Finally there are the chat
sessions, which are the saved conversations between user and bot, for future training of our models.
"""

user_docs = """
These routes are designed for looking at ingested sites, and the documents therein. We can upload new documents, one by
one or in batch. We can then choose to summarize any of those documents individually. Future functionality will include
the ability to upload from emails.
"""

reco_update = """
These routes are for the recommendation engine which is integral to the work done with the bots and ingestion. This
will constantly help us improve our models and ability to aid the client in the most efficient way.
"""

tags_metadata = [
    {
        "name": "health",
        "description": "The endpoints listed here check to make sure the connection is established properly. For internal use.",
    },
    {
        "name": "login",
        "description": """For logging in to use the other endpoints available.
        You can also use the `Authorize` button shown in the top right of this screen""",
    },
    {
        "name": "upload",
        "description": """These endpoints are for uploading individual or multiple documents at a time.
        You can also choose to summarize an already uploaded document or view a site already processed.
        Uploading emails is not available yet.""",
    },
    {"name": "bots", "description": bots_sdks_deploys},
    {"name": "deployments", "description": bots_sdks_deploys},
    {"name": "sdks", "description": bots_sdks_deploys},
    {
        "name": "web-ingest",
        "description": """The routes here contain the functionality of the web scraping and data extraction from a set
        websites/urls requested by the user and not contained within our blacklist (generally social media sites).
        There are options to scrape and extract from one page at a time, multiple sites or a single site and all their
        connected sites.""",
    },
    {"name": "user", "description": user_docs},
    {"name": "documents", "description": user_docs},
    {"name": "/api/v1", "description": "See Health, Login."},
    {"name": "recommendation", "description": reco_update},
    {"name": "update", "description": reco_update},
    {
        "name": "read",
        "description": "See user, documents for viewing and summarizing documents.",
    },
]

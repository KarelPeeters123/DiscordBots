import json

from objects.election import Election
class ElectionService:
    def __init__(self):
        self.read()

    def read(self):
        try:
            with open('elections.json', 'r') as f:
                self.election_dict = json.load(f)
        except:
            self.election_dict = {}
            self.write()
    def write(self):
        with open('elections.json', 'w') as f:
            json.dump(self.election_dict, f, indent=4)

    def add_election(self, election):
        self.read()
        self.election_dict[election.id] = election.__dict__
        self.write()

    def get_election(self, election_id):
        return Election(json=self.election_dict[election_id])

    def register(self, election_id, user):
        self.read()
        self.get_election(election_id).register(user)
        self.write()
    def unregister(self, election_id, user):
        self.read()
        self.get_election(election_id).unregister(user)
        self.write()

    async def vote(self, bot, payload, vote_id, election_id, selected):
        self.read()
        print(self.get_election(election_id).can_vote(payload, vote_id, selected))
        if self.get_election(election_id).can_vote(payload, vote_id, selected):
            await self.get_election(election_id).vote(bot, payload, vote_id, selected)
        self.write()

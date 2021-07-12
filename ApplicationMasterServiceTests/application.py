import json
class Application:
    def __init__(self, applicationId, affectedFields, applicationChemaVersion, completedTreatments, applicationPatch):
        self.ApplicationId = applicationId,
        self.AffectedFields = affectedFields,
        self.ApplicationSchemaVersion = applicationChemaVersion,
        self.CompletedTreatments = completedTreatments,
        self.ApplicationPatch = applicationPatch
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
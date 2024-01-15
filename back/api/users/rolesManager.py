class rolesManager():
    roles = [
        {
            "name": "admin",
            "title": "Super-Administrador",
            "contains": ["administrator", "viewer", "manager", "user", "guest"],
        },
        {
            "name": "administrator",
            "title": "Administrador",
            "contains": ["viewer", "manager", "user", "guest"],
        },
        {
            "name": "manager",
            "title": "Gestor de rutas",
            "contains": ["user", "guest", "viewer"],
        },
        {
            "name": "viewer",
            "title": "Usuario Visor",
            "contains": ["user", "guest"],
        },

    ]

    @staticmethod
    def hasPermission(requestedRole, userRole):
        if requestedRole == userRole:
            return True
        for rol in rolesManager.roles:
            if rol["name"] == userRole:
                if requestedRole in rol["contains"]:
                    return True
        return False

    @staticmethod
    def getRolesList():
        returnList = []
        for rol in rolesManager.roles:
            returnList.append((rol["name"], rol["title"]))
        return returnList

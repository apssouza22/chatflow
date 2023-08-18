from datetime import date

from core.cost.cost_dao import CostDao, Cost, sum_cost


class CostService:
    def __init__(self, cost_dao: CostDao):
        self.cost_dao = cost_dao

    def get_user_costs(self, user: str) -> dict:
        return self.cost_dao.get(user)

    def put_cost(self, cost: Cost, user_email: str, app_key: str):
        existing_cost = self.get_user_costs(user_email)
        app_model = app_key + "_" + cost.model
        today = f"today_{date.today()}"
        if not existing_cost:
            self.cost_dao.put(user_email, {
                app_model: {today: cost.dict()}
            })
            return

        if app_model not in existing_cost:
            existing_cost[app_model] = {today: cost.dict()}
            self.cost_dao.put(user_email, existing_cost)
            return

        if today in existing_cost[app_model]:
            current_cost = Cost(**existing_cost[app_model][today])
            current_cost = sum_cost([current_cost, cost])
            existing_cost[app_model][today] = current_cost.dict()
            self.cost_dao.put(user_email, existing_cost)
            return

        existing_cost[app_model][today] = cost.dict()
        self.cost_dao.put(user_email, existing_cost)

    def has_allowance_exceeded(self, user_email, app_key):
        existing_cost = self.get_user_costs(user_email)
        today = f"today_{date.today()}"
        for model in existing_cost:
            if model.startswith(app_key) and "gpt-4" in model:
                if existing_cost[model].get(today):
                    cost = Cost(**existing_cost[model][today])
                    return cost.total_tokens > 100_000

            if model.startswith(app_key) and "gpt-3" in model:
                if existing_cost[model].get(today):
                    cost = Cost(**existing_cost[model][today])
                    return cost.total_tokens > 900_000

        return False


def cost_service_factory() -> CostService:
    return CostService(CostDao())

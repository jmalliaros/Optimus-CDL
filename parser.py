def parse_optimization_model(user_string, compiler_type="manual"):
	formulation = None
	constraints = []

	if compiler_type == "manual":

		for t in user_string.split("\n"):
			if t.startswith("minimize") or t.startswith("maximize"):
				formulation = t.split(" ")[1:]
				break
		for t in user_string.split("\n"):
			if t.startswith("subject to"):
				constraints.append(t.split(" ")[2:])

		return formulation, constraints


if __name__ == "__main__":
	d = """
minimize 5*x + 8*x
subject to x>=1
	"""
	print(parse_optimization_model(d.strip()))

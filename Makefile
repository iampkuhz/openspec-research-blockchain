.PHONY: install-skills change-primitive validate-schema

install-skills:
	./scripts/install_repo_skills.sh

change-primitive:
	./scripts/new_change.sh primitive "$(NAME)"

validate-schema:
	openspec schema validate blockchain-research

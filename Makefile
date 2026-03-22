.PHONY: install-skills change-domain change-primitive change-synthesis change-decision scan-language validate-schema

install-skills:
	./scripts/install_repo_skills.sh

change-domain:
	./scripts/new_change.sh domain "$(NAME)"

change-primitive:
	./scripts/new_change.sh primitive "$(NAME)"

change-synthesis:
	./scripts/new_change.sh synthesis "$(NAME)"

change-decision:
	./scripts/new_change.sh decision "$(NAME)"

scan-language:
	./scripts/scan_language.sh

validate-schema:
	openspec schema validate blockchain-research

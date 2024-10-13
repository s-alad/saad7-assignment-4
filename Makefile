.PHONY: install run

install:
	# Backend setup
	cd backend && python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt && \
	python preprocess.py
	# Frontend setup
	cd frontend && npm install

run:
	# Start backend server in the background
	cd backend && \
	. venv/bin/activate && \
	python app.py &
	# Start frontend server in the background
	cd frontend && \
	npm run dev &
	# Wait for servers to start
	sleep 10

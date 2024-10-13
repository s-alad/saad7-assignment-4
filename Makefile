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
	nohup python app.py > backend.log 2>&1 &
	# Start frontend server in the background
	cd frontend && \
	npm run dev > frontend.log 2>&1 &
	# Wait for servers to start
	sleep 10

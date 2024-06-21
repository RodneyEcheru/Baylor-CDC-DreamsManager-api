import uvicorn

if __name__ == "__main__":

    # run app on port depending on whether it's running on localhost or production
    try:
        uvicorn.run("app.main:app", host="62.171.141.19", port=5001, reload=True, log_level="debug", reload_dirs=["app"])  # production server
    except:
        uvicorn.run("app.main:app", host="127.0.0.1", port=5001, reload=True, log_level="debug", reload_dirs=["app"])  # development server

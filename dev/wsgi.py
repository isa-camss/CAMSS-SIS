from main import app
import cfg.ctt as ctt


if __name__ == '__main__':
    app.run(port=ctt.API_PORT, debug=ctt.API_DEBUG)

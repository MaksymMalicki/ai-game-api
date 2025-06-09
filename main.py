import uvicorn
import argparse
from server import app
import game_generators
import game_engine

NO_OPENAI = False

# For testing purpouses or no OpenAi Tokens disable API ussage 
# The code sets global NO_OPENAI to True, when would like to diesble OpenAI Api calls
def parse_args():
    parser = argparse.ArgumentParser(description="Run your game engine")
    parser.add_argument(
        "-no-openai", "--no-openai",
        action="store_true",
        help="Run in offline mode without OpenAI API calls"
    )
    return parser.parse_args()

if __name__ == "__main__":
    ## Check if user wont to run app with NO OPENAI flag
    args = parse_args()
    NO_OPENAI = args.no_openai
    # Propagate the offline flag to other modules that use OpenAI
    game_generators.NO_OPENAI = NO_OPENAI
    game_engine.NO_OPENAI = NO_OPENAI
    # Run app
    uvicorn.run(app, host="127.0.0.1", port=8001)

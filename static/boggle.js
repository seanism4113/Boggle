class BoggleGame {
	/* make a new game */

	constructor(boardId, seconds = 60) {
		this.seconds = seconds; // game length
		this.showTimer();

		this.score = 0;
		this.words = new Set();
		this.board = $("#" + boardId);

		this.timer = setInterval(this.tick.bind(this), 1000);

		$(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
	}

	showWord(word) {
		$(".words", this.board).append($("<li>", { text: word }));
	}

	showScore() {
		$(".score", this.board).text(this.score);
	}

	showMessage(message, cls) {
		$(".message", this.board)
			.text(message)
			.removeClass()
			.addClass(`message ${cls}`);
	}

	// Handle the submission of a word and return erroror if necessary

	async handleSubmit(evt) {
		evt.preventDefault();
		const $word = $(".word", this.board);

		let word = $word.val();
		if (!word) return;

		if (this.words.has(word)) {
			this.showMessage(`Already found ${word}`, "error");
			return;
		}

		const resp = await axios.get("/check-word", { params: { word: word } });
		if (resp.data.result === "not-word") {
			this.showMessage(`${word} is not a valid English word`, "error");
		} else if (resp.data.result === "not-on-board") {
			this.showMessage(`${word} is not a valid word on this board`, "error");
		} else {
			this.showWord(word);
			this.score += word.length;
			this.showScore();
			this.words.add(word);
			this.showMessage(`Added: ${word}`, "ok");
		}

		$word.val("").focus();
	}

	showTimer() {
		$(".timer", this.board).text(this.seconds);
	}

	// Timer handling.  If timer is up game is over

	async tick() {
		this.seconds -= 1;
		this.showTimer();

		if (this.seconds === 0) {
			clearInterval(this.timer);
			await this.scoreGame();
		}
	}

	// At the end of Game, show messages for score, highscore and post score to server

	async scoreGame() {
		$(".add-word", this.board).hide();
		const resp = await axios.post("/post-score", { score: this.score });
		if (resp.data.newRecord) {
			this.showMessage(`New record: ${this.score}`, "ok");
		} else {
			this.showMessage(`Final score: ${this.score}`, "ok");
		}
	}
}

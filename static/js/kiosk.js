(function () {
  document.addEventListener("alpine:init", () => {
    Alpine.data("kioskSession", (config) => ({
      prompt: false,
      timer: null,
      graceTimer: null,
      init() {
        const poke = () => {
          this.prompt = false;
          this.arm();
        };
        ["pointerdown", "keydown", "touchstart"].forEach((name) => {
          document.addEventListener(name, poke, { capture: true });
        });
        document.body.addEventListener("htmx:afterSwap", () => this.arm());
        this.arm();
      },
      get active() {
        const experience = document.getElementById("experience");
        return !!experience && !!experience.querySelector("[data-guard='1']");
      },
      arm() {
        clearTimeout(this.timer);
        clearTimeout(this.graceTimer);
        if (!this.active) {
          this.prompt = false;
          return;
        }
        this.timer = setTimeout(() => {
          this.prompt = true;
          this.graceTimer = setTimeout(() => {
            if (typeof htmx !== "undefined") {
              htmx.ajax("POST", config.resetUrl, {
                target: "#experience",
                swap: "innerHTML",
              });
            }
          }, config.grace * 1000);
        }, config.stillThere * 1000);
      },
    }));

    Alpine.data("kioskCountdown", (seconds, resetUrl) => ({
      remaining: seconds,
      init() {
        this.intervalId = setInterval(() => {
          this.remaining -= 1;
          if (this.remaining <= 0) {
            clearInterval(this.intervalId);
            if (typeof htmx !== "undefined") {
              htmx.ajax("POST", resetUrl, {
                target: "#experience",
                swap: "innerHTML",
              });
            }
          }
        }, 1000);
      },
      destroy() {
        clearInterval(this.intervalId);
      },
    }));

    Alpine.data("kioskReveal", () => ({
      show: false,
      init() {
        this.$nextTick(() => {
          requestAnimationFrame(() => {
            this.show = true;
          });
        });
      },
    }));

    Alpine.data("kioskPress", () => ({
      pressed: false,
      down() {
        this.pressed = true;
      },
      up() {
        this.pressed = false;
      },
    }));
  });
})();

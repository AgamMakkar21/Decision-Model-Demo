from html import escape

import streamlit as st


STYLES = """
<style>
:root {
    --paper: #F4F2E9;
    --ink: #203D34;
    --pine: #1C443A;
    --persimmon: #A54429;
    --muted: #5C6D61;
    --line: #D7DCCE;
    --surface: #FEFDF8;
    --track: #E5E8DC;
    --border: #B3BDAE;
    --button-base: #102D25;
    --button-hover: #2A5949;
    --on-color: #FEFDF8;
    --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
    --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
    --desk-font: "Open Sans", "Segoe UI", sans-serif;
    --heading-font: "Bubblegum Sans", "Segoe UI", sans-serif;
    --radius: .3rem;
    --radius-small: .15rem;
}
.stApp {
    background: var(--paper);
    color: var(--ink);
    font-family: var(--desk-font);
}
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stFileUploaderFileName"] { color: var(--ink); }
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] p { color: var(--muted); }
.stApp [data-testid="stCaptionContainer"] { opacity: 1; }
.stApp :is(button, [role="tab"]) [data-testid="stMarkdownContainer"] { color: inherit; }
.stApp [data-testid="stBaseButton-secondary"],
.stApp [data-testid="stBaseButton-secondaryFormSubmit"] {
    background: var(--surface);
    color: var(--pine);
    border-color: var(--border);
}
.stApp [data-testid="stExpander"] details { border-color: var(--line); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMain"] { scrollbar-gutter: stable; }
[data-testid="stMainBlockContainer"] {
    max-width: 1120px;
    padding: 3.5rem 2rem 2rem;
}
.desk-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: .5rem;
    border-bottom: 1px solid var(--pine);
}
.desk-brand {
    display: flex;
    align-items: center;
    gap: .65rem;
    font-family: var(--heading-font);
    font-weight: 400;
    font-size: 1.4rem;
}
.desk-note { color: var(--muted); font-size: .85rem; }
.desk-intro {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 8rem;
    align-items: center;
    gap: 1.5rem;
    padding: 1rem 1.5rem;
    margin: 1rem 0 0;
    background: var(--pine);
    border-radius: var(--radius);
    box-shadow: 5px 5px 0 var(--persimmon), 8px 10px 18px #203D3412;
}
.desk-intro h1 {
    font-family: var(--heading-font);
    font-weight: 400;
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    line-height: 1;
    letter-spacing: 0;
    padding: 0 0 .5rem;
    margin: 0;
    color: var(--on-color);
    text-wrap: balance;
}
.desk-intro p {
    margin: 0;
    max-width: 40ch;
    color: var(--paper);
    line-height: 1.6;
}
.desk-mail-art {
    position: relative;
    height: 5.5rem;
    color: var(--paper);
}
.desk-mail-art::before, .desk-mail-art::after {
    content: "";
    position: absolute;
    right: 0;
    width: 2rem;
    height: 1.5rem;
    border: 2px solid currentColor;
    border-left: 0;
}
.desk-mail-art::before { top: .5rem; }
.desk-mail-art::after { bottom: .5rem; }
.desk-letter {
    position: absolute;
    top: 1rem;
    left: .25rem;
    width: 5.5rem;
    height: 3.5rem;
    border: 2px solid var(--paper);
    border-radius: var(--radius-small);
    background: var(--pine);
    transform: rotate(-8deg);
    box-shadow: 4px 5px 0 var(--persimmon), 7px 8px 12px #102D2540;
    overflow: hidden;
}
.desk-letter::before {
    content: "";
    position: absolute;
    width: 4rem;
    height: 4rem;
    left: .6rem;
    top: -2.4rem;
    border-right: 2px solid var(--paper);
    border-bottom: 2px solid var(--paper);
    transform: rotate(45deg);
}
.desk-letter::after {
    content: "";
    position: absolute;
    right: .4rem;
    bottom: .4rem;
    width: .75rem;
    height: .85rem;
    background: var(--persimmon);
    border: 1px solid var(--paper);
}
[role="tablist"] {
    position: relative;
    isolation: isolate;
    width: min(100%, 22rem);
    gap: 0;
    padding: .35rem .35rem 0;
    background: var(--track);
    border-radius: var(--radius) var(--radius) 0 0;
    border-bottom: 1px solid var(--pine);
}
[role="tablist"]::before {
    content: "";
    position: absolute;
    z-index: -1;
    top: .35rem;
    bottom: 0;
    left: .35rem;
    width: calc(50% - .35rem);
    background: var(--pine);
    border: 1px solid var(--pine);
    border-bottom: 0;
    border-radius: var(--radius-small) var(--radius-small) 0 0;
    box-shadow: inset 0 -3px 0 var(--persimmon);
    transform: translateX(0);
    pointer-events: none;
}
[role="tablist"]:has([role="tab"]:nth-child(2)[aria-selected="true"])::before {
    transform: translateX(100%);
}
[role="tablist"][data-pointer-motion="true"]::before {
    transition: transform 250ms var(--ease-in-out);
}
[role="tablist"] [role="tab"] {
    flex: 1 1 0;
    min-width: 0;
    justify-content: center;
    padding: .75rem .5rem;
    background: transparent;
    border: 0;
    color: var(--muted);
}
[role="tablist"] [role="tab"][aria-selected="true"] { color: var(--on-color); }
[role="tablist"] [role="tab"] p { font-weight: 700; }
[role="tablist"] [role="tab"]::before {
    content: "";
    flex-shrink: 0;
    width: .9rem;
    height: .65rem;
    margin-right: .55rem;
    border: 1.5px solid currentColor;
    border-radius: var(--radius-small);
    transform: rotate(-8deg);
}
[role="tablist"] [role="tab"]:nth-child(2)::before {
    box-shadow: 2px -3px 0 -1px var(--track), 2px -3px 0 0 currentColor;
}
[role="tablist"][data-pointer-motion="true"] [role="tab"]::before {
    transition: transform 160ms var(--ease-out);
}
[role="tablist"] [role="tab"][aria-selected="true"]::before {
    transform: translateY(-1px) rotate(0);
}
[role="tablist"][data-pointer-motion="true"] [role="tab"]:active::before {
    transform: scale(.9);
}
[role="tablist"] .react-aria-SelectionIndicator { display: none; }
[role="tablist"] [role="tab"]:focus-visible {
    outline: 2px solid var(--persimmon);
    outline-offset: -4px;
    border-radius: var(--radius-small) var(--radius-small) 0 0;
}
[data-testid="stForm"], .st-key-batch_input {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    box-shadow: 3px 4px 0 var(--line), 5px 7px 16px #203D3408;
}
[data-testid="stWidgetLabel"] p {
    font-family: var(--desk-font);
    font-weight: 700;
    font-size: .95rem;
}
[data-testid="stFileUploaderDropzone"] {
    background: var(--track);
    color: var(--ink);
    border: 1px dashed var(--pine);
    border-radius: var(--radius-small);
}
[data-testid="stFileUploaderDropzone"] small { color: var(--muted); }
[data-testid="stTextAreaRootElement"] {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--paper);
    overflow: hidden;
}
[data-testid="stTextAreaRootElement"]:focus-within {
    border-color: var(--pine);
    outline: 2px solid var(--pine);
    outline-offset: -2px;
}
[data-testid="stTextArea"] textarea {
    font-family: var(--desk-font);
    font-size: 1rem;
    line-height: 1.6;
    color: var(--ink);
    background: var(--paper);
    caret-color: var(--pine);
    border-radius: var(--radius-small);
    padding-bottom: 2rem;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: var(--muted);
    opacity: 1;
}
:is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button {
    background: var(--pine);
    color: var(--on-color);
    border: 1px solid var(--pine);
    border-radius: var(--radius);
    min-height: 2.85rem;
    max-width: 100%;
    padding: .6rem 1.1rem;
    box-shadow: 0 5px 0 var(--button-base), 0 8px 12px #203D3418;
    transform: translateY(-2px);
    transition: transform 160ms var(--ease-out);
}
:is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button::before {
    content: "";
    flex-shrink: 0;
    width: 1.05rem;
    height: .75rem;
    margin-right: .3rem;
    border: 1.5px solid currentColor;
    border-radius: var(--radius-small);
    background: linear-gradient(32deg, transparent 47%, currentColor 49% 53%, transparent 55%)
        left top / 50% 70% no-repeat,
        linear-gradient(-32deg, transparent 47%, currentColor 49% 53%, transparent 55%)
        right top / 50% 70% no-repeat;
    transform: rotate(-8deg);
    transition: transform 160ms var(--ease-out);
}
:is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button::after {
    content: "";
    flex-shrink: 0;
    width: .4rem;
    height: .4rem;
    margin-left: .3rem;
    border-top: 2px solid currentColor;
    border-right: 2px solid currentColor;
    transform: rotate(45deg);
    transition: transform 160ms var(--ease-out);
}
:is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) {
    padding-top: 2px;
    padding-bottom: 4px;
}
:is(.st-key-sample_email, .st-key-batch_actions [data-testid="stDownloadButton"]) {
    padding-top: 2px;
    padding-bottom: 4px;
}
:is(.st-key-sample_email, .st-key-batch_actions [data-testid="stDownloadButton"]) button {
    min-height: 2.85rem;
    padding: .6rem 1.1rem;
    border-radius: var(--radius);
    transform: translateY(-2px);
    box-shadow: 0 4px 0 var(--line), 0 6px 10px #203D3410;
    transition: transform 160ms var(--ease-out);
}
:is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button:not(:disabled):active:not(:focus-visible) {
    transform: translateY(3px) scale(.97);
}
:is(.st-key-sample_email, .st-key-batch_actions [data-testid="stDownloadButton"]) button:active:not(:focus-visible) {
    transform: translateY(2px) scale(.97);
}
:is([data-testid="stFormSubmitButton"], .st-key-batch_actions) button:focus-visible {
    transition: none;
    transform: none;
}
:is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button p {
    font-family: var(--desk-font);
    font-weight: 700;
    white-space: normal;
    min-width: 0;
}
:is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button:focus-visible {
    outline: 3px solid var(--persimmon);
    outline-offset: 3px;
}
:is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button:disabled {
    background: var(--line);
    color: var(--muted);
    border-color: var(--line);
    box-shadow: none;
    transform: none;
}
[class*="st-key-decision_panel"], [class*="st-key-gpt_panel"] {
    --model-color: var(--pine);
    border: 1px solid var(--model-color);
    border-radius: var(--radius);
    background: var(--surface);
    padding: 1rem;
    gap: .75rem;
    min-width: 0;
}
[class*="st-key-gpt_panel"] { --model-color: var(--persimmon); }
.batch-email-heading {
    font-family: var(--heading-font);
    font-weight: 400;
    color: var(--model-color, var(--pine));
    font-size: 1.35rem;
    padding: .5rem 0 .25rem;
    margin: 0;
}
.batch-email-preview {
    color: var(--muted);
    font-size: .9rem;
    line-height: 1.5;
    max-width: 75ch;
    overflow-wrap: anywhere;
    margin: 0;
}
.model-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .75rem;
    flex-wrap: wrap;
    margin: -1rem -1rem .25rem;
    padding: .75rem 1rem;
    background: var(--model-color);
    border-radius: var(--radius-small) var(--radius-small) 0 0;
}
.model-heading h2 {
    font-family: var(--heading-font);
    font-weight: 400;
    color: var(--on-color);
    font-size: 1.85rem;
    letter-spacing: 0;
    margin: 0;
    padding: 0;
}
.model-heading span { font-size: .8rem; color: var(--on-color); }
.model-status {
    display: flex;
    align-items: center;
    gap: .5rem;
    color: var(--muted);
    font-size: .875rem;
    min-height: 1.5rem;
    opacity: 1;
    transition: opacity 180ms var(--ease-out);
}
.model-status::before {
    content: "";
    width: .5rem;
    height: .5rem;
    flex-shrink: 0;
    border-radius: 50%;
    background: var(--muted);
}
.model-status.is-loading { min-height: 3rem; gap: .75rem; }
.model-status.is-loading::before { display: none; }
.dispatch-envelope {
    position: relative;
    flex: 0 0 auto;
    width: 2rem;
    height: 1.5rem;
    border: 2px solid currentColor;
    border-radius: var(--radius-small);
    overflow: hidden;
    color: var(--model-color, var(--pine));
    animation: dispatch-mail 1200ms linear infinite;
}
.dispatch-envelope::before {
    content: "";
    position: absolute;
    width: 1.25rem;
    height: 1.25rem;
    left: .25rem;
    top: -.75rem;
    border-right: 2px solid currentColor;
    border-bottom: 2px solid currentColor;
    transform: rotate(45deg);
}
@keyframes dispatch-mail {
    0%, 100% { transform: translateY(0); opacity: .7; }
    50% { transform: translateY(-3px); opacity: 1; }
}
@starting-style {
    .model-status { opacity: 0; }
}
.result-metrics {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.25fr);
    gap: 1rem;
    margin: 0;
    padding: .25rem 0 .75rem;
    border-bottom: 1px solid var(--line);
    font-variant-numeric: tabular-nums;
    opacity: 1;
    transition: opacity 180ms var(--ease-out);
}
@starting-style {
    .result-metrics { opacity: .7; }
}
.result-metrics dt { font-size: .8rem; color: var(--muted); }
.result-metrics dd {
    margin: .25rem 0 0;
    font-size: clamp(1.05rem, 2vw, 1.45rem);
    font-weight: 700;
    color: var(--ink);
    overflow-wrap: anywhere;
}
.result-metrics small { font-size: .75rem; font-weight: 400; }
.st-key-decision_panel [data-testid="stCaptionContainer"],
.st-key-gpt_panel [data-testid="stCaptionContainer"] {
    color: var(--muted);
    font-variant-numeric: tabular-nums;
}
.likelihood p { font-size: .85rem; line-height: 1.4; margin: 0 0 .35rem; }
.likelihood-track {
    height: .8rem;
    background: var(--track);
    border-radius: var(--radius-small);
    overflow: hidden;
}
.likelihood-fill {
    width: 100%;
    height: 100%;
    background: var(--model-color);
}
.stApp:has(:focus-visible) .result-metrics { transition: none; }
.st-key-decision_panel details, .st-key-gpt_panel details {
    scroll-margin-block: 4rem 1rem;
}
.st-key-decision_panel summary, .st-key-gpt_panel summary {
    transition: transform 160ms var(--ease-out);
}
.st-key-decision_panel summary:active:not(:focus-visible),
.st-key-gpt_panel summary:active:not(:focus-visible) {
    transform: scale(.99);
}
@media (hover: hover) and (pointer: fine) {
    :is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button:not(:disabled):hover {
        background: var(--button-hover);
        color: var(--on-color);
        border-color: var(--button-hover);
    }
    :is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button:not(:disabled):hover:not(:active):not(:focus-visible) {
        transform: translateY(-3px);
    }
    :is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button:not(:disabled):hover:not(:active):not(:focus-visible)::before {
        transform: translate(2px, -2px) rotate(0);
    }
    :is(.st-key-send_email, .st-key-batch_actions [data-testid="stButton"]) button:not(:disabled):hover:not(:active):not(:focus-visible)::after {
        transform: translateX(3px) rotate(45deg);
    }
    :is(.st-key-sample_email, .st-key-batch_actions [data-testid="stDownloadButton"]) button:hover:not(:active):not(:focus-visible) {
        transform: translateY(-3px);
    }
}
@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] { padding: 3rem 1rem 2rem; }
    .desk-note { display: none; }
    .desk-intro {
        grid-template-columns: minmax(0, 1fr);
        padding: 1rem;
        margin-top: 1rem;
        gap: 0;
    }
    .desk-mail-art { display: none; }
    .result-metrics dd { font-size: 1.2rem; }
}
@media (prefers-reduced-motion: reduce) {
    [role="tablist"][data-pointer-motion="true"]::before { transition: none; }
    [role="tablist"] [role="tab"]::before {
        transition: none !important;
        transform: none !important;
    }
    .dispatch-envelope { animation: none; }
    :is([data-testid="stFormSubmitButton"], .st-key-batch_actions) button {
        transition: none !important;
        transform: none !important;
    }
    :is([data-testid="stFormSubmitButton"], .st-key-batch_actions) button::before,
    :is([data-testid="stFormSubmitButton"], .st-key-batch_actions) button::after {
        transition: none !important;
        transform: none !important;
    }
    .model-status { transition-duration: 100ms; }
    .result-metrics,
    .st-key-decision_panel summary,
    .st-key-gpt_panel summary { transition: none; }
    .st-key-decision_panel summary:active,
    .st-key-gpt_panel summary:active { transform: none !important; }
    @starting-style {
        .model-status { opacity: .8; }
    }
}
</style>
"""


DETAILS_SCRIPT = """
<script>
(() => {
    window.dispatchDeskController?.abort();
    const controller = new AbortController();
    window.dispatchDeskController = controller;
    const pointerOpened = new WeakSet();
    const detailsSelector = ".st-key-decision_panel details, .st-key-gpt_panel details";
    const fillSelector = ".likelihood-fill";
    const reducedMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

    document.addEventListener("pointerdown", event => {
        if (!(event.target instanceof Element)) return;
        const list = event.target.closest('[role="tablist"]');
        if (!list) return;
        list.dataset.pointerMotion = String(!reducedMotion());
        getComputedStyle(list, "::before").transform;
    }, {capture: true, signal: controller.signal});

    document.addEventListener("keydown", event => {
        if (!(event.target instanceof Element)) return;
        const list = event.target.closest('[role="tablist"]');
        if (list) list.dataset.pointerMotion = "false";
    }, {capture: true, signal: controller.signal});

    document.addEventListener("click", event => {
        if (!(event.target instanceof Element)) return;
        const tab = event.target.closest('[role="tab"]');
        if (tab) {
            const list = tab.closest('[role="tablist"]');
            list.dataset.pointerMotion = String(event.detail > 0 && !reducedMotion());
        }
        const details = event.target.closest("summary")?.parentElement;
        if (!details?.matches(detailsSelector)) return;
        if (event.detail > 0) pointerOpened.add(details);
        else pointerOpened.delete(details);
        requestAnimationFrame(() => details.getAnimations().forEach(animation => {
            if (event.detail > 0 && !reducedMotion()) {
                animation.effect.updateTiming({duration: 200});
            } else {
                animation.finish();
            }
        }));
    }, {capture: true, signal: controller.signal});

    document.addEventListener("toggle", event => {
        const details = event.target;
        if (!(details instanceof HTMLDetailsElement) || !details.matches(detailsSelector)) return;
        const fills = details.querySelectorAll(fillSelector);
        fills.forEach(fill => fill.getAnimations().forEach(animation => animation.cancel()));
        if (!details.open) return;

        requestAnimationFrame(async () => {
            const animate = pointerOpened.has(details) && !reducedMotion();
            const easing = getComputedStyle(details).getPropertyValue("--ease-out").trim();
            const sweeps = animate ? [...fills].map(fill => {
                const sweep = fill.animate(
                    [{transform: "translateX(-100%)"}, {transform: fill.style.transform}],
                    {duration: 500, easing}
                );
                sweep.pause();
                sweep.currentTime = 0;
                return sweep;
            }) : [];
            await new Promise(requestAnimationFrame);
            let opening = details.getAnimations();
            while (opening.some(animation => animation.playState === "running")) {
                opening.forEach(animation => {
                    if (animate) animation.effect.updateTiming({duration: 200});
                    else animation.finish();
                });
                await Promise.allSettled(opening.map(animation => animation.finished));
                await new Promise(requestAnimationFrame);
                if (controller.signal.aborted || !details.isConnected || !details.open) return;
                opening = details.getAnimations();
            }
            requestAnimationFrame(() => {
                if (controller.signal.aborted || !details.isConnected || !details.open) return;
                if (animate && sweeps.every(sweep => sweep.playState === "idle")) return;
                const play = () => {
                    if (controller.signal.aborted || !details.isConnected || !details.open) return;
                    sweeps.filter(sweep => sweep.playState === "paused").forEach(sweep => sweep.play());
                };
                const scroller = details.closest('[data-testid="stMain"]');
                const box = details.getBoundingClientRect();
                const viewport = scroller.getBoundingClientRect();
                const style = getComputedStyle(details);
                const topMargin = parseFloat(style.scrollMarginTop);
                const bottomMargin = parseFloat(style.scrollMarginBottom);
                const top = box.top - viewport.top - topMargin;
                const bottom = box.bottom - viewport.bottom + bottomMargin;
                const tooTall = box.height > scroller.clientHeight - topMargin - bottomMargin;
                const delta = top < 0 || tooTall ? top : Math.max(0, bottom);
                const target = Math.max(0, Math.min(
                    scroller.scrollHeight - scroller.clientHeight, scroller.scrollTop + delta
                ));
                const smooth = animate && "onscrollend" in scroller
                    && Math.abs(target - scroller.scrollTop) > 1;
                if (smooth) scroller.addEventListener("scrollend", play, {
                    once: true, signal: controller.signal
                });
                scroller.scrollTo({top: target, behavior: smooth ? "smooth" : "instant"});
                if (!smooth) play();
            });
        });
    }, {capture: true, signal: controller.signal});
})();
</script>
"""


def show_intro():
    st.html(STYLES)
    st.html("""
        <header class="desk-header">
            <div class="desk-brand">
                Dispatch desk
            </div>
            <span class="desk-note">Email classification demo</span>
        </header>
        <div class="desk-intro">
            <div>
                <h1>Email Demo</h1>
                <p>Compare urgency, routing, time and cost.</p>
            </div>
            <div class="desk-mail-art" aria-hidden="true">
                <span class="desk-letter"></span>
            </div>
        </div>
    """ + DETAILS_SCRIPT, unsafe_allow_javascript=True)


def show_model_heading(model, description):
    st.html(
        f'<div class="model-heading"><h2>{escape(model)}</h2>'
        f'<span>{escape(description)}</span></div>'
    )


def show_email_heading(number, email):
    preview = " ".join(email.split())
    if len(preview) > 160:
        preview = preview[:160] + "..."
    st.html(
        f'<h3 class="batch-email-heading">Email {number}</h3>'
        f'<p class="batch-email-preview">{escape(preview)}</p>'
    )


def show_status(message, loading=False):
    envelope = (
        '<span class="dispatch-envelope" aria-hidden="true"></span>'
        if loading else ""
    )
    status_class = "model-status is-loading" if loading else "model-status"
    st.html(
        f'<div class="{status_class}" role="status">{envelope}<span>{escape(message)}</span></div>'
    )


def show_metrics(seconds, cost):
    cost_text = f"${cost:.8f} <small>USD</small>" if cost is not None else "Unavailable"
    st.html(
        '<dl class="result-metrics">'
        f'<div><dt>API time</dt><dd>{seconds:.3f} <small>sec</small></dd></div>'
        f'<div><dt>Estimated cost</dt><dd>{cost_text}</dd></div>'
        '</dl>'
    )


def show_probability(label, score):
    # Match the label's precision so 100.0% always fills the entire track.
    percentage = round(score * 100, 1)
    st.html(
        '<div class="likelihood">'
        f'<p>{escape(label)}: {percentage:.1f}%</p>'
        f'<div class="likelihood-track" role="progressbar" aria-label="{escape(label)}" '
        f'aria-valuenow="{percentage:.1f}" aria-valuemin="0" aria-valuemax="100">'
        f'<div class="likelihood-fill" style="transform: translateX({percentage - 100:.1f}%);"></div>'
        '</div></div>'
    )

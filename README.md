# Email decision demo

A small, Python-only Streamlit app comparing two existing Foundry deployments:
`Decision-1` and `gpt-6-sol`. Paste an email and select **Send to both models**.
Both calls run concurrently, and each result appears as soon as it finishes.

Each model panel shows its selected urgency and department with likelihoods,
API-call time, and estimated USD cost. Expand **Likelihoods & token usage** to
see every label's likelihood as a horizontal bar and the reported token counts.
No tests or test framework are included.

The **Single email** tab keeps this full comparison. In **Batch emails**, upload
a UTF-8 CSV with one email per row and a column named `email` (case-insensitive).
Other columns are ignored. Download the sample CSV in the app for 10 short
example emails covering a mix of urgency levels and all three departments.
Put email bodies containing commas or line breaks inside double quotes:

```csv
email
"Our email server is down. Please restore service immediately."
"Please send the benefits guide, when convenient."
```

Select **Send batch to both models** to send all rows in one request to each
deployment: two requests total, submitted concurrently. This is prompt batching,
not ten independent calls per model.
Results are grouped by model, with Email 1, Email 2, and so on listed underneath.
Each email shows the selected urgency and department, including their winning
likelihoods. **Batch API time** appears once per model and measures its entire
request, not any individual email's latency. There are no per-email times,
per-option bars, token counts, or costs in the batch results. Email previews
identify the rows, and each model's list keeps the CSV's order. Blank emails
and malformed CSV rows are reported before any model calls begin.
Quoted multiline emails and UTF-8 files with a byte-order mark are supported.

Both models receive the same numbered emails in a shared JSON state. Decision
asks two named `Choice` questions per email in one `system_one` call (20 questions
for 10 emails). GPT returns a strict JSON object with one classification per
email ID in one Responses API call. Questions explicitly target each email's
own body, but all emails share context, unlike isolated single-email requests.
Every submitted ID and probability distribution must be present and valid.

Batch mode reuses single-email mode's question definitions, probability
validation, request clients, and cached authentication. Each model's complete
batch appears as soon as its request finishes; a failed batch is shown against
that model without discarding the other model's results. There is no automatic
fallback to per-email calls. Switching tabs preserves both sets of results for
the browser session. This does not use an asynchronous Batch API or discounted
batch pricing. Large CSVs remain subject to each deployment's input, question,
output, and rate limits; unsupported requests are shown as errors.

## Run

Use Python 3.10+ and [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
on your laptop. Sign in with your Microsoft Entra account in the FDPO tenant.
No managed identity, API key, or Azure hosting is needed.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
az login --tenant "<your-FDPO-tenant-ID>"
az account set --subscription "<subscription-containing-your-Foundry-resource>"
.\.venv\Scripts\python -m streamlit run app.py
```

Open the address printed by Streamlit, normally `http://localhost:8501`.
On Windows ARM, use an x64 Python installation if Streamlit's dependencies do
not have ARM64 wheels (for example, `py -3.12-64 -m venv .venv`).

The resource endpoint and deployment names are already set at the top of
`app.py`, using the supplied starter snippets:

- Resource: `https://ai-call-demo-decision-resource.services.ai.azure.com`
- Decision deployment: `Decision-1`
- GPT deployment: `gpt-6-sol`
- Token scope: `https://ai.azure.com/.default`

## Microsoft Entra authentication

The app uses `AzureCliCredential` to obtain tokens for the account signed in
through `az login`. This deliberately uses your local CLI login, not managed
identity or a credential fallback chain. The SDK argument named `api_key`
receives a short-lived Entra bearer token, not an API key. There are no API keys
or client secrets to configure, and `AZURE_CLIENT_ID` is not used.

1. Sign in to the tenant that owns the Foundry resource using the commands above.
   The tenant ID is available in Azure Portal under **Microsoft Entra ID > Overview**.
2. Grant your signed-in user inference access to the Foundry resource. For example,
   use **Cognitive Services User** at the resource scope; the GPT endpoint may
   also require **Cognitive Services OpenAI User**, depending on your role
   configuration. Follow your tenant administrator's approved RBAC policy and
   allow a few minutes for new role assignments to propagate.
3. Ensure your laptop can reach the Foundry endpoint. If public access is disabled,
   use your organization's approved VPN/private network connection.

If authentication expires, run `az login --tenant "<your-FDPO-tenant-ID>"` again.
If inference returns HTTP 403 after sign-in, check your user permissions and the
resource's network rules. Entra user authentication must be allowed by your
tenant policy; it is keyless, but it is not managed identity.

The bearer-token provider is cached in memory with `st.cache_resource`, so
subsequent submissions reuse a valid token instead of invoking Azure CLI again.
Azure Identity automatically refreshes the token near expiry. The first request
and later refreshes still need authentication. The cached provider is shared
across browser sessions in this local app process; restart Streamlit after
switching CLI accounts or tenants to discard the previous account's token.
Token acquisition remains outside the measured model API calls.

Authentication and model errors appear in the UI and are logged to the server
console. Keep the demo private to its intended audience; it has no app-level
sign-in. Email text is sent only to the configured Azure resource. GPT response
storage is disabled; Azure's applicable service logging and retention policies
still apply.

## How to read the comparison

Both models receive the same email content, questions, label definitions, and
allowed categories. In single-email mode, Decision uses two `Choice` questions in one `system_one`
request, rather than a binary `Noul`, because each question has three options.
GPT uses one Responses API call with a strict JSON schema. The highest
probability in each group determines the displayed label; a tie uses label
order. Invalid distributions are reported as errors, not silently normalized.
Bar lengths use the same one-decimal percentage as their labels, so a displayed
100.0% fills the entire track. This display rounding does not change model outputs.

**Likelihoods are not equivalent measurements.** Decision returns native model
probabilities. GPT generates self-reported likelihood estimates; they are not
token log probabilities or independently calibrated confidence scores.

**Time** is measured with `perf_counter()` around each SDK call. It includes
network travel and SDK request/response processing, but excludes token
acquisition, client construction, display, and local result validation. Both
SDKs have a 60-second timeout and automatic retries disabled. The two requests
are submitted concurrently, not guaranteed to reach the service at the exact
same instant. Cold connections, service load, region, token count, and caching
can affect results. Repeat with representative emails before drawing conclusions;
this is an interactive demo, not a controlled benchmark.

**Estimated cost** uses the supplied flat rates:

| Model | USD per million total tokens |
| --- | ---: |
| Decision-1 | $0.042 |
| GPT-6-Sol | $2.00 |

```text
estimated cost = (reported input tokens + reported output tokens) * rate / 1,000,000
```

These rates apply equally to input and output tokens, as a demo assumption.
You can change them in `PRICES` at the top of `app.py`. If your deployment
charges different input/output rates, this flat-rate estimate is not your
invoice. Cache discounts, taxes, negotiated billing adjustments, and failed-call
charges are not calculated. GPT's reported output usage includes any reasoning
tokens billed by the service; the app does not estimate usage from visible text.
If an API omits token usage, cost is shown as unavailable, never as zero.

Classification and authentication are in `app.py`; presentation helpers and
embedded CSS are in `ui.py`. A small embedded browser script handles likelihood
bar sweeps and scrolling expanded details into view. Streamlit still supplies
the native textbox, button, and responsive two-column layout; `ui.py` renders
the probability bars without truncating them to whole percentages.
No additional dependencies, externally hosted fonts, or UI build step is needed.

The "Dispatch desk" interface uses warm ivory, pine green for Decision-1, and
persimmon for GPT, with subtly rounded corners, Bubblegum Sans headings, and
Open Sans body text. Both fonts are bundled in `static/` and served locally,
with their SIL Open Font Licenses in `static/BubblegumSans-OFL.txt` and
`static/OpenSans-OFL.txt`. Segoe UI / sans-serif provides fallback glyphs.
The pine title panel uses a static envelope-and-routing motif; matching pine and
persimmon model headers make the comparison easy to scan. The motif is hidden
on small screens to keep the email composer prominent.
Send buttons have a raised base and a 160 ms downward press that works with
mouse and touch. Browser-style tabs slide only their selected surface in 250 ms;
the content stays still, and a stable scrollbar gutter prevents horizontal jumps
between shorter and longer views. Keyboard tab switching is instant.
While a model request is pending, a gently moving
envelope indicates activity, not estimated progress; it disappears on completion
or error. Likelihood tracks are thicker for easier reading.
Reduced-motion preferences remove the sliding, button movement, and envelope
motion. All feedback stays outside measured API-call times.
The likelihood disclosure has subtle pointer-press feedback.
Disclosures open and close in 200 ms. Model statuses and arriving metrics fade
briefly. Opening likelihood details
with a pointer sweeps the bars to their reported percentages in 500 ms; labels
and numbers remain immediately readable and do not count up. Expanded details
scroll into view when needed, then replay the sweep on every opening.
Keyboard-opened details and reduced-motion mode
use instant scrolling without bar sweeps; keyboard focus and reduced-motion
preferences also disable metric fades.

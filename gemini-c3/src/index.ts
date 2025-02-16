/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Bind resources to your worker in `wrangler.jsonc`. After adding bindings, a type definition for the
 * `Env` object can be regenerated with `npm run cf-typegen`.
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export default {
	async fetch(request: string, env) {
	  const url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent";
	  const apiKey = env.GEMINI_API_KEY;
  
	  const body = JSON.stringify({
		contents: [{ parts: [{ text: request }] }]
	  });
  
	  const response = await fetch(`${url}?key=${apiKey}`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body
	  });
  
	  const data = await response.json();
	  return new Response(JSON.stringify(data), {
		headers: { "Content-Type": "application/json" }
	  });
	}
  };
  
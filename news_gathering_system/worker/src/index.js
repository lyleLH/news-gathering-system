export default {
  async fetch(request, env) {
    // For simplicity, we'll only handle GET requests to /api/inspirations
    if (request.method === "GET" && request.url.includes("/api/inspirations")) {
      const responseData = {"data": [
        {
          "title": "A Decade of Slug",
          "url": "https://terathon.com/blog/decade-slug.html"
        },
        {
          "title": "Python 3.15's JIT is now back on track",
          "url": "https://fidget-spinner.github.io/posts/jit-on-track.html"
        },
        {
          "title": "Get Shit Done: A Meta-Prompting, Context Engineering and Spec-Driven Dev System",
          "url": "https://github.com/gsd-build/get-shit-done"
        },
        {
          "title": "Microsoft's 'unhackable' Xbox One has been hacked by 'Bliss'",
          "url": "https://www.tomshardware.com/video-games/console-gaming/microsofts-unhackable-xbox-one-has-been-hacked-by-bliss-the-2013-console-finally-fell-to-voltage-glitching-allowing-the-loading-of-unsigned-code-at-every-level"
        },
        {
          "title": "Warranty Void If Regenerated",
          "url": "https://nearzero.software/p/warranty-void-if-regenerated"
        }
      ]};
      
      const headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*" // Allow all origins for now
      };
      
      return new Response(JSON.stringify(responseData), { headers, status: 200 });
    }

    return new Response("Not Found", { status: 404 });
  },
};
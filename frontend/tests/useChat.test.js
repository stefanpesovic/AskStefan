import { renderHook, act, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import useChat from "../src/hooks/useChat";

vi.mock("../src/api/client", () => ({
  default: {
    post: vi.fn(),
  },
}));

vi.mock("react-hot-toast", () => ({
  default: {
    error: vi.fn(),
    success: vi.fn(),
  },
}));

import api from "../src/api/client";
import toast from "react-hot-toast";

describe("useChat", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("starts with empty state", () => {
    const { result } = renderHook(() => useChat());
    expect(result.current.messages).toEqual([]);
    expect(result.current.currentSources).toEqual([]);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.lastQuery).toBe("");
  });

  it("sends message and receives response", async () => {
    api.post.mockResolvedValueOnce({
      data: {
        answer: "I know Python and JavaScript.",
        sources: [
          {
            chunk_id: "cv_pdf__page_1__0",
            source_file: "cv.pdf",
            source_type: "resume",
            location: "page 1",
            text: "Python developer",
            similarity_score: 0.9,
          },
        ],
        latency_ms: 500,
        model: "llama-3.3-70b-versatile",
      },
    });

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage("What are your skills?");
    });

    expect(result.current.messages).toHaveLength(2);
    expect(result.current.messages[0].role).toBe("user");
    expect(result.current.messages[0].content).toBe("What are your skills?");
    expect(result.current.messages[1].role).toBe("assistant");
    expect(result.current.messages[1].content).toBe(
      "I know Python and JavaScript."
    );
    expect(result.current.currentSources).toHaveLength(1);
    expect(result.current.isLoading).toBe(false);
  });

  it("sets loading state during request", async () => {
    let resolvePost;
    api.post.mockReturnValueOnce(
      new Promise((resolve) => {
        resolvePost = resolve;
      })
    );

    const { result } = renderHook(() => useChat());

    let sendPromise;
    act(() => {
      sendPromise = result.current.sendMessage("Test question");
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(true);
    });

    await act(async () => {
      resolvePost({
        data: { answer: "Answer", sources: [], latency_ms: 100, model: "test" },
      });
      await sendPromise;
    });

    expect(result.current.isLoading).toBe(false);
  });

  it("shows toast on 429 rate limit", async () => {
    api.post.mockRejectedValueOnce({
      response: { status: 429 },
    });

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage("Test");
    });

    expect(toast.error).toHaveBeenCalledWith(
      "I'm getting a lot of questions — please wait a moment"
    );
    expect(result.current.messages).toHaveLength(0);
  });

  it("shows toast on network error", async () => {
    api.post.mockRejectedValueOnce({
      code: "ERR_NETWORK",
    });

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage("Test");
    });

    expect(toast.error).toHaveBeenCalledWith(
      "Connection issue. Please try again."
    );
  });

  it("auto-triggers ingest on 503", async () => {
    api.post
      .mockRejectedValueOnce({ response: { status: 503 } })
      .mockResolvedValueOnce({});

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage("Test");
    });

    expect(toast.error).toHaveBeenCalledWith(
      "Indexing documents... please try again in a moment."
    );
    expect(api.post).toHaveBeenCalledWith("/ingest");
  });

  it("ignores empty or whitespace-only messages", async () => {
    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage("   ");
    });

    expect(result.current.messages).toHaveLength(0);
    expect(api.post).not.toHaveBeenCalled();
  });

  it("updates lastQuery on send", async () => {
    api.post.mockResolvedValueOnce({
      data: { answer: "Answer", sources: [], latency_ms: 100, model: "test" },
    });

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage("What projects?");
    });

    expect(result.current.lastQuery).toBe("What projects?");
  });
});

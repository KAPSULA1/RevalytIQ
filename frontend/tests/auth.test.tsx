import { render, fireEvent, waitFor, screen } from "@testing-library/react";
import { useRouter } from "next/navigation";

import SignupPage from "../app/signup/page";
import { register, api } from "../lib/auth";

jest.mock("../lib/auth", () => {
  const actualModule = jest.requireActual("../lib/auth") as typeof import("../lib/auth");

  return {
    ...actualModule,
    register: jest.fn(
      (...args: Parameters<typeof actualModule.register>) =>
        actualModule.register(...args),
    ),
  };
});

jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));

const mockedRegister = register as jest.MockedFunction<typeof register>;
const mockedUseRouter = useRouter as jest.MockedFunction<typeof useRouter>;

describe("register API helper", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("posts the registration payload and returns user data", async () => {
    const responseData = {
      id: 1,
      username: "newuser",
      email: "newuser@example.com",
    };
    const postSpy = jest
      .spyOn(api, "post")
      .mockResolvedValueOnce({ data: responseData } as any);

    await expect(register("newuser", "newuser@example.com", "password123")).resolves.toEqual(
      responseData,
    );
    expect(postSpy).toHaveBeenCalledWith("/api/auth/register/", {
      username: "newuser",
      email: "newuser@example.com",
      password: "password123",
    });

    postSpy.mockRestore();
  });

  it("throws when the backend rejects the request", async () => {
    const error = new Error("Username already exists");
    const postSpy = jest.spyOn(api, "post").mockRejectedValueOnce(error);

    await expect(register("existing", "existing@example.com", "password123")).rejects.toThrow(
      "Username already exists",
    );
    expect(postSpy).toHaveBeenCalledTimes(1);

    postSpy.mockRestore();
  });
});

describe("SignupPage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("redirects to login after successful registration", async () => {
    const pushMock = jest.fn();
    mockedUseRouter.mockReturnValue({ push: pushMock } as any);
    mockedRegister.mockResolvedValueOnce({
      id: 1,
      username: "newuser",
      email: "newuser@example.com",
    });

    render(<SignupPage />);

    fireEvent.change(screen.getByPlaceholderText("Username"), {
      target: { value: " newuser " },
    });
    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: " newuser@example.com " },
    });
    fireEvent.change(screen.getByPlaceholderText("Password"), {
      target: { value: "password123" },
    });

    fireEvent.submit(screen.getByTestId("signup-form"));

    await waitFor(() =>
      expect(mockedRegister).toHaveBeenCalledWith("newuser", "newuser@example.com", "password123"),
    );
    expect(pushMock).toHaveBeenCalledWith("/");
  });
});

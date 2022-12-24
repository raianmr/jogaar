import { useRouter } from "next/router"
import { FormEvent, useEffect, useState } from "react"
import { tokenDataFetcher } from "../data/fetching"
import { getToken, setToken } from "../data/store"

// TODO https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/

export default function Login() {
  const router = useRouter()

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [errorMsg, setErrorMsg] = useState("")

  useEffect(() => {
    const token = getToken()

    if (token) {
      router.push("/modmins")
    }
  })

  const submitHandler = async (e: FormEvent) => {
    e.preventDefault()

    try {
      const data = await tokenDataFetcher({ username, password })

      setErrorMsg("")
      setToken(data)

      router.push("/modmins")
    } catch (e: any) {
      setErrorMsg(e.message)
    }
  }

  return (
    <main>
      <form className="form-signin" onSubmit={submitHandler}>
        <h1 className="h3 mb-3 font-weight-normal text-center">
          Enter credentials
        </h1>
        <input
          type="email"
          className="form-control"
          placeholder="Email"
          required
          onChange={e => setUsername(e.target.value)}
        />
        <input
          type="password"
          className="form-control"
          placeholder="Password"
          required
          onChange={e => setPassword(e.target.value)}
        />

        <button className="w-100 btn btn-lg btn-primary" type="submit">
          Sign in
        </button>

        {errorMsg && (
          <p className="p-1 mt-2 w-100 alert alert-danger text-center">
            {errorMsg}
          </p>
        )}
      </form>
    </main>
  )
}

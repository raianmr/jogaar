import { useRouter } from "next/router"
import { FormEvent, useState } from "react"
import { fetchTokenData } from "../data/fetching"
import { setToken } from "../data/store"

// TODO read and implement https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/

export default function Login() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [errorMsg, setErrorMsg] = useState("")
  const router = useRouter()

  const submit = async (e: FormEvent) => {
    e.preventDefault()

    try {
      const data = await fetchTokenData(username, password)

      setErrorMsg("")
      setToken(data)
      console.log(data)

      router.push("/dashboard")
    } catch (e: any) {
      setErrorMsg(e.data.detail)
    }
  }

  return (
    <main>
      <form className="form-signin" onSubmit={submit}>
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

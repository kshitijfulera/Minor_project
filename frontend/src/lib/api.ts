export async function uploadLevel(formData: FormData) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload-level`, {
        method: "POST",
        body: formData
    })
    return res.json()
}
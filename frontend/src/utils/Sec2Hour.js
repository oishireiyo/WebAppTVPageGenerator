export default function sec2Hour(sec) {
  const hour = Math.floor(sec / (60 * 60))
  const min = Math.floor(sec / 60) % 60
  const secrem = Math.floor(sec % 60)

  return {
    hour: hour,
    min: min,
    sec: secrem,
  }
}
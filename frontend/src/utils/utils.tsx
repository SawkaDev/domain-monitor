export const formatDate = (dateString: string | null) => {
  if( dateString === null ) {
    return 'n/a';
  }
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const SeaPointInfoCard = ({ name }) => {
  return (
    <div className='relative bg-slate-100 p-5 rounded shadow-md mb-4 hover:bg-slate-300'>
      <h2 className='text-xl font-bold'>{name}</h2>
    </div>
  );
};

export default SeaPointInfoCard;

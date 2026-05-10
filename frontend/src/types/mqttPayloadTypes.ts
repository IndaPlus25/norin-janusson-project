export type ObservationCreatedEvent = {
  observation_id: number;
};

export type CarObservationCreatedRefEvent = {
  car_observation_id: number;
};

export type CarObservationUpdatedEvent = {
  car_observation_id: number;
  observation_id: number;
};

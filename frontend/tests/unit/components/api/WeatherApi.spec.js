import { apiGetWeather } from '@/components/api/WeatherApi';

describe('api for weather data from tomorrow.io', () => {

  it('gets weather data',
    async () => {
      const pos = {
        coords: {
          latitude: 5.322528,
          longitude: 100.282142
        }
      }
      let data = null
      let error = null
      await apiGetWeather(pos)
        .then((res) => {
          data = res.data;
        })
        .catch((err) => {
          error = err;
        });

      expect(error).toBeNull();
      expect(data).toBeInstanceOf(Object);
      expect(data).toHaveProperty('timelines');
      expect(data.timelines).toBeInstanceOf(Array);
      expect(data.timelines).toHaveLength(2);

      const weatherProperties = [
        'humidity',
        'windSpeed',
        'temperature',
        'cloudCover',
        'weatherCode'
      ]

      expect(data.timelines[0]).toHaveProperty('startTime');
      expect(data.timelines[0]).toHaveProperty('endTime');
      expect(data.timelines[0]).toHaveProperty('timestep', 'current');
      expect(data.timelines[0].intervals).toBeInstanceOf(Array);
      expect(data.timelines[0].intervals[0]).toHaveProperty('startTime');
      expect(data.timelines[0].intervals[0]).toHaveProperty('values');
      expect(Object.keys(data.timelines[0].intervals[0].values)).toEqual(
        expect.arrayContaining(weatherProperties));

      expect(data.timelines[1]).toHaveProperty('startTime');
      expect(data.timelines[1]).toHaveProperty('endTime');
      expect(data.timelines[1]).toHaveProperty('timestep', '1h');
      expect(data.timelines[1].intervals).toBeInstanceOf(Array);
      expect(data.timelines[1].intervals[0]).toHaveProperty('startTime');
      expect(data.timelines[1].intervals[0]).toHaveProperty('values');
      expect(Object.keys(data.timelines[1].intervals[0].values)).toEqual(
        expect.arrayContaining(weatherProperties));
    });
});

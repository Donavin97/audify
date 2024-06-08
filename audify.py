import argparse
from obspy import read
from obspy.clients.fdsn import Client
import obspy.signal
import numpy as np

# Function to Sonify seismic data
def sonify(args):
    # Initialize FDSN client
    client = Client(args.client)
    
    # Fetch inventory first
    inv = client.get_stations(network=args.network,
                              station=args.station,
                              location=args.location,
                              channel=args.channel,
                              level="response")
    
    # Get waveforms after fetching inventory
    stream = client.get_waveforms(network=args.network,
                                  station=args.station,
                                  location=args.location,
                                  channel=args.channel,
                                  starttime=args.start_time,
                                  endtime=args.end_time)
    
    # Merge streams
    stream.merge(fill_value='interpolate')
    
    # Remove response from inventory
    stream.remove_response(inventory=inv, taper=0.01)
    
    # Detrend data
    stream.detrend('demean')
    
    # Filter data
    stream.filter('bandpass', freqmin=args.fmin, freqmax=args.fmax, zerophase=True)
# Generate the envelope
    env = obspy.signal.filter.envelope(stream[0].data)
    
    # Adjust speed factor
    stream.interpolate(sampling_rate=44100/args.speed_factor, method='lanczos', a=20)
    stream.taper(0.01)

    # Save to WAV file
    stream.write(args.outputfile, format='WAV', width=2, rescale=True, framerate=44100)
#    env.write(env.wav, format='WAV', framerate=44100, width=2, rescale=True)
    print(env)
    print(f"Data processed and saved to {args.outputfile}")

# Main execution block
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sonify seismic data.")
    parser.add_argument('-C', '--client', type=str, required=True, help='fdsn cliet for retrieving seismic waveform data. E.G. iris, gfz http://localhost:88080.')
    parser.add_argument('-n', '--network', type=str, required=True, help='Network code.')
    parser.add_argument('-s', '--station', type=str, required=True, help='Station code.')
    parser.add_argument('-l', '--location', type=str, required=True, help='Location code.')
    parser.add_argument('-c', '--channel', type=str, required=True, help='Channel code.')
    parser.add_argument('-f', '--fmin', type=float, required=True, help='Minimum frequency of the filter.')
    parser.add_argument('-F', '--fmax', type=float, required=True, help='Maximum frequency of the filter.')
    parser.add_argument('-S', '--speed-factor', type=float, required=True, help='Speed factor for adjusting sample rate.')
    parser.add_argument('-o', '--outputfile', type=str, required=True, help='Output file.wav format.')
    parser.add_argument('-t', '--timespan', type=str, required=True, help='Start time and end time e.g., "2024-05-25 00:00~2024-05-25 01:00"')
    
    args = parser.parse_args()
    
    # Parse timespan into start_time and end_time
    start_time_str, end_time_str = args.timespan.split('~')
    # Convert string times to datetime objects
    from obspy.core.utcdatetime import UTCDateTime
    start_time = UTCDateTime(start_time_str+":00")
    end_time = UTCDateTime(end_time_str+":00")
    
    # Update the arguments with the converted datetime objects
    args.start_time = start_time
    args.end_time = end_time
    
    # Further processing based on the timespan could be done here if needed
    sonify(args)

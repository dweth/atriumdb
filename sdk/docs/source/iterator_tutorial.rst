Reading Datasets with Iterators
===============================

Working with large datasets often requires efficient access to smaller windows of data, particularly for tasks such
as data visualization, pre-processing, or model training. The AtriumSDK provides a convenient method, `get_iterator`,
to handle these cases effectively. This tutorial will guide you through the end-to-end process of setting up the
AtriumSDK instance, creating a `DatasetDefinition` object, and iterating over data windows.


Setting Up the SDK Instance
---------------------------

First things first, let's set up the SDK:

.. code-block:: python

    from atriumdb import AtriumSDK

    local_dataset_location = "/path/to/your/dataset"
    sdk = AtriumSDK(dataset_location=local_dataset_location)

Creating a Dataset Definition
-----------------------------

The `DatasetDefinition` object specifies the measures, patients, or devices and the time intervals we are interested in querying.
This definition can be provided in two different ways: by reading from a YAML file or by creating the object in your Python script.

**Option 1: Using a YAML file**

Suppose you have the following in your `definition.yaml` file:

.. code-block:: yaml

    patient_ids:
      1001: all
      1002:
        - start: 1682739200000000000  # nanosecond Unix Epoch Time
          end: 1682739300000000000    # End time

    measures:
      - MDC_ECG_LEAD_I
      - tag: MDC_TEMP
        freq_hz: 1.0
        units: 'MDC_DIM_DEGC'

You can load this into a `DatasetDefinition` object as follows:

.. code-block:: python

    from atriumdb import DatasetDefinition

    definition = DatasetDefinition(filename="definition.yaml")


**Option 2: Creating an object via Python script**

Alternatively, you can define your dataset programmatically:

.. code-block:: python

    from atriumdb import DatasetDefinition

    measures = ['MDC_ECG_LEAD_I',
                {"tag": "MDC_TEMP", "freq_hz": 1.0, "units": "MDC_DIM_DEGC"},]
    patient_ids = {
        1001: 'all',
        1002: [{'start': 1682739200000000000, 'end': 1682739300000000000}]
    }

    definition = DatasetDefinition(measures=measures, patient_ids=patient_ids)

If you wanted to create a dataset of all patients born after a certain date, you could setup your patient_ids dictionary like:

.. code-block:: python

    min_dob = 1572739200000000000  # Nanosecond epoch
    patient_ids = {patient_id: "all" for patient_id, patient_info in
        sdk.get_all_patients().items() if patient_info['dob'] and patient_info['dob'] > min_dob}

Iterating Over Windows
----------------------

Now that we've setup the `DatasetDefinition` object, we can use it to iterate over our dataset.

.. code-block:: python

    window_size_nano = 60 * 1_000_000_000  # Define window size in nanoseconds (60 seconds)
    slide_size_nano = 30 * 1_000_000_000  # Define slide size in nanoseconds for overlapping windows if necessary (30 seconds)

    # Obtain the iterator
    iterator = sdk.get_iterator(definition, window_size_nano, slide_size_nano)

    # Now you can iterate over the data windows
    for window_i, window in enumerate(iterator):
        print(f"Window: {window_i}")
        print(f"Start Time: {window.start_time}")
        print(f"Device ID: {window.device_id}")
        print(f"Patient ID: {window.patient_id}")

        # Use window.signals to view available signals in their original form
        for (measure_tag, measure_freq_nhz, measure_units), signal_dict in window.signals.items():
            print(f"Measure: {measure_tag}, Frequency: {measure_freq_nhz}, Units: {measure_units}")
            print(f"Times: {signal_dict['times']}")
            print(f"Values: {signal_dict['values']}")
            print(f"Expected Count: {signal_dict['expected_count']}")
            print(f"Actual Count: {signal_dict['actual_count']}")

        # Use the array_matrix for a single matrix containing all signals
        data_matrix = iterator.get_array_matrix(window_i)
        print(data_matrix)
